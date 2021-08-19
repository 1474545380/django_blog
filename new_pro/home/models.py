from django.db import models
from django.utils import timezone
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