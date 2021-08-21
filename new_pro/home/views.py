from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from home.models import ArticleCategory
from django.http.response import HttpResponseNotFound
from home.models import Article,Comment
from django.core.paginator import Paginator,EmptyPage
# Create your views here.

class IndexView(View):
    def get(self,request):
        # 获取所有分类信息
        categories=ArticleCategory.objects.all()
        # 接收用户点击的分类id
        cat_id=request.GET.get('cat_id',1)
        # 根据分类id进行分类查询
        try:
            category=ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')
        # 获取分页参数
        page_num=request.GET.get('page_num',1)
        page_size=request.GET.get('page_size',10)
        # 根据分类信息查询文章数据
        articles=Article.objects.filter(category=category)
        # 创建分页器
        paginator=Paginator(object_list=articles,per_page=page_size)
        # 进行分页处理
        try:
            page_articles=paginator.page(page_num)
        except EmptyPage as e:
            return HttpResponseNotFound('emptypage')
        #总页数
        total_page=paginator.num_pages
        # 组织数据传递给模版
        context={
            "categories": categories,
            'category':category,
            'articles':page_articles,
            'page_size':page_size,
            'total_page':total_page,
            'page_num':page_num
        }
        return render(request,'index.html',context=context)

#文章详情页面
class DetailView(View):
    #文章详情
    def get(self,request):
        #获取搜索的id
        id=request.GET.get('id')
        article = Article
        #查询文章
        try:
            article=Article.objects.get(id=id)
        except Article.DoesNotExist:
            return  render(request,'404.html')
        else:
            #浏览量加一
            article.total_views+=1
            article.save()
        #分类数据
        categorties=ArticleCategory.objects.all()

        #查询浏览量前十的文章
        hot_articles=Article.objects.order_by('-total_views')[:9]
        # 获取分页请求参数
        page_size=request.GET.get('page_size',10)
        page_num=request.GET.get('page_num',1)
        # 根据文章信息查询评论数据
        comments=Comment.objects.filter(article=article).order_by('-created')
        #获取评论总数
        total_count=comments.count()
        # 创建分页器
        paginator=Paginator(comments,page_size)
        # 分页处理
        try:
            page_comments=paginator.page(page_num)
        except:
            return HttpResponseNotFound('empty page')
        #获取总页数
        total_page=paginator.num_pages
        context={
            'categories':categorties,
            'category':article.category,
            'article':article,
            'hot_articles':hot_articles,
            'total_count':total_count,
            'comments':page_comments,
            'page_size':page_size,
            'total_page':total_page,
            'page_num':page_num
        }
        return render(request,'detail.html',context=context)
    #文章评论
    def post(self,request):
        # 接收用户信息
        user=request.user
        # 判断用户是否登陆
        if user and user.is_authenticated:
        # 登陆则接收form数据
            # 接收评论数据
            id=request.POST.get('id')
            content=request.POST.get('content')
            #验证文章是否存在
            try:
                article=Article.objects.get(id=id)
            except Article.DoesNotExist:
                return  render(request,'404.html')
            #保存评论数据
            Comment.objects.create(
                content=content,
                article=article,
                user=user,
                )
            #修改文章评论数量
            article.comments_count+=1
            article.save()
            #重定向
            path=reverse('home:detail')+'?id={}'.format(article.id)
            return redirect(path)
        else:
            # 未登陆跳转到登陆页面
            return redirect(reverse('users:login'))
