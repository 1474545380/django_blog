from django.db import models
from django.utils import timezone
from users.models import User
# Create your models here.
#写文章
class ArticleCategory(models.Model):
    #标题
    title=models.CharField(max_length=100,blank=True)
    #分类的创建时间
    created=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    class Meta:
        #修改表名
        db_table='tb_category'
        #admin站点显示，方便查看对象
        verbose_name='类别管理'
        verbose_name_plural=verbose_name
#文章模型
class Article(models.Model):
    #作者，on_delete：当user表中数据删除后，文章信息也同步删除
    auth=models.ForeignKey(User,on_delete=models.CASCADE)
    #标题图
    avatar=models.ImageField(upload_to='artice/%Y%m%d',blank=True)
    #标题
    title=models.CharField(max_length=20,blank=True)
    #栏目
    category=models.ForeignKey(ArticleCategory,null=True,blank=True,on_delete=models.CASCADE,related_name='article')
    #标签
    tags=models.CharField(max_length=20,blank=True)
    #摘要信息
    sumary=models.CharField(max_length=200,null=False,blank=False)
    #文章正文
    content=models.TextField()
    #浏览量
    total_views=models.PositiveSmallIntegerField(default=0)
    #评论量
    comments_count=models.PositiveSmallIntegerField(default=0)
    #文章创建时间
    created=models.DateTimeField(default=timezone.now)
    #文章修改时间
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        #修改表名
        db_table='tb_article'
        ordering=('-created',)
        verbose_name='文章管理'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title
#写文章
class Comment(models.Model):
    # 评论内容
    content=models.TextField()
    # 评论文章
    article=models.ForeignKey(Article,on_delete=models.SET_NULL,null=True)
    # 评论用户
    user=models.ForeignKey('users.User',on_delete=models.SET_NULL,null=True)
    # 评论时间
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.article.title
    class Meta:
        db_table='tb_comment'
        verbose_name='评论管理'
        verbose_name_plural=verbose_name