from django.conf.urls import patterns, include, url
from django.contrib import admin
from myblog import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','blog.views.handlehome',name='home'),
    url(r'^blog/$','blog.views.handleblogmain',name='blog'),
    url(r'^blog/article/(?P<id>\d+)/$','blog.views.handleblogcontent',name='showArticle'),
    url(r'^blog/tags/(?P<tags>\w+\+*)/$','blog.views.handletags',name='showTag'),
    url(r'^account/verifycode/$','blog.views.handleverifycode',name='verifyCode'),
    url(r'^account/verifyemail/$','blog.views.handleverifyemail',name='verifyEmail'),
    url(r'^postcomment/$','blog.views.postcomment',name='postcomment'),
    url(r'^account/oauth/(?P<sitename>\w+)/$','blog.views.callback',name='callback'),
    
    url(r'^account/login/?$', 'blog.views.login', name="login"),
    url(r'^account/logout/?$', 'blog.views.logout', name="logout"),
    url(r'^account/login/error/?$', 'blog.views.login_error', name="login_error"),
    url(r'^account/register/?$', 'blog.views.register', name="register"),
    url(r'^account/register2/?$', 'blog.views.register_step_2', name="register_step_2"),
        
    url(r'^test/$','blog.views.handletest'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
    #url(r'', include('social_login.urls')),


)
