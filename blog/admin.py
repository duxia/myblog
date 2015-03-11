#coding=UTF-8
from django.contrib import admin
from django.db.models import F
from blog.models import article, articletypeList, comment
from mptt.admin import MPTTModelAdmin

# Register your models here.
class commentInline(admin.StackedInline):
    model = comment
    
class articleAdmin(admin.ModelAdmin):
    list_display = ('title','articletype','publishdate',)
    search_fields = ('title','articletype',)
    ordering = ('-publishdate',)
    fields = ('title','content','articletype','istop','clicknums','commentnums',)
    inlines = [commentInline,]
    #自定义save函数
    def save_model(self, request, obj, form, change):
        if not change: #(新增文章时，对应的文章类型数量自动+1)
            articletype = articletypeList.objects.get(typename=obj.articletype)
            articletype.articleNums =F('articleNums') + 1 #原子性的修改,等同于articleNums+=1
            articletype.save()
        obj.save()
    #自定义delete函数
    def delete_model(self, request, obj): #删除文章时,对应文章类型数量自动-1
        articletype = articletypeList.objects.get(typename=obj.articletype)
        articletype.articleNums =F('articleNums') - 1
        articletype.save()
        obj.delete()
    
    
class articletypeListAdmin(admin.ModelAdmin):
    list_display = ('typename','articleNums',)
    fields = ('typename',)
    #自定以save函数
    def save_model(self, request, obj, form, change):
        if change:
            obj_original=self.model.objects.get(pk=obj.pk)
            obj.articleNums=obj_original.articleNums
        else:
            obj.articleNums=0 #将添加的文章类型数量默认为0
        obj.save()
        
class commentAdmin(MPTTModelAdmin):    
    list_display = ('username','Usericon','usercomment','parentarticle')
    search_fields = ('username','usercomment',)
    ordering = ('parentarticle','publicdate',)
    fields = ('username','usercomment','parentarticle')
    
    def Usericon(self,obj):
        return '<img src="%s" />' % obj.usericon
    Usericon.allow_tags = True
    
    def delete_model(self, request, obj):
        parentarticle = article.objects.get(title=obj.parentarticle)
        parentarticle.commentnums = F('commentnums') - 1
        parentarticle.save()
        obj.delete()
    
admin.site.register(article, articleAdmin)
admin.site.register(articletypeList,articletypeListAdmin)
#评论
#admin.site.register(comment,MPTTModelAdmin)
admin.site.register(comment,commentAdmin)