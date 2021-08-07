from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.
class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True,blank=False)
    avatar=models.ImageField(upload_to='avatar/%Y%m%d',blank=True)
    #个人简介
    user_desc=models.CharField(max_length=500,blank=True)
    class Meta:
        #修改表名
        db_table='tb_users'
        #后台显示
        verbose_name='用户管理'
        #后台显示
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.mobile