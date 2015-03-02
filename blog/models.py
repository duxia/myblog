#coding=UTF-8
from django.db import models
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from social_login.abstract_models import AbstractInnerUserAuth, AbstractUserInfo
# from social_login.abstract_models import AbstractInnerUserAuth, AbstractUserInfo

# Create your models here.
class articletypeList(models.Model):
    typename = models.CharField(max_length=30)
    articleNums = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = '文章类型'
    
    def __unicode__(self):
        return self.typename
    
class article(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField('content')
    publishdate = models.DateField(auto_now_add=True) #首次创建时自动加入当前时间
    articletype = models.ForeignKey(articletypeList)
    istop = models.BooleanField(default=False)
    clicknums = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
    
    def __unicode__(self):
        return self.title

#评论
class comment(MPTTModel):
    username = models.CharField(max_length=50)
    usericon = models.CharField(max_length=255, blank=True)
    usercomment = models.TextField()
    parentarticle = models.ForeignKey(article) #评论对应的文章
    publicdate = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
    def __unicode__(self):
        return self.usercomment
    
class UserAuth(AbstractInnerUserAuth):
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=128)
     
class UserInfo(AbstractUserInfo):
    pass

