#coding=utf-8
from django.shortcuts import render, render_to_response
from blog.models import article, articletypeList, comment
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from PIL import Image


from social_login.models import SiteUser

# as same as SiteUser, import the following two just for this example
# to get the siet_name_zh
from socialoauth import SocialSites
from socialoauth.utils import import_oauth_class
from myblog.settings import SOCIALOAUTH_SITES
from socialoauth.exception import SocialAPIError
from myblog import settings
import os
import time
from blog.forms import CaptchaForm
from django.views.decorators.csrf import csrf_exempt

class RegisterLoginError(Exception):
    pass

from .models import UserAuth, UserInfo
# Create your views here.
#首页页面
def handlehome(request):
    return render_to_response('blog_home.html')

#认证回调页面
def callback(request,sitename):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("oauth2 login error!")
    
    socialsites = SocialSites(SOCIALOAUTH_SITES)
    s = socialsites.get_site_object_by_name(sitename)
    try:
        s.get_access_token(code)
    except SocialAPIError as e:
        print e.site_name
        print e.url
        print e.error_msg
        raise
    
    print s.uid
    print s.name
    return HttpResponse("uid="+s.uid+"; name="+s.name)

#博客列表主页面
def handleblogmain(request):
    articles = article.objects.values('id','title','articletype__typename','publishdate','istop','clicknums')
    articletypes = articletypeList.objects.all()
    toparticlelist=articles.order_by('-publishdate')[0:5] #右边栏最新文章
    topviewlist = articles.order_by('clicknums')[0:10] #右边栏阅读排行
    recentcomments = comment.objects.values('username','usercomment','parentarticle__title','parentarticle__id').order_by('-publicdate')[0:5] #最新评论
    #将文章和所对应的评论表关联(获取评论数)
    def _make_article_info(_article):
        info = {}
        info['id'] = _article['id']
        info['title'] = _article['title']
        info['articletype__typename'] = _article['articletype__typename']
        info['publishdate'] = _article['publishdate']
        info['istop'] = _article['istop']
        info['clicknums'] = _article['clicknums']
        info['commentnums'] = comment.objects.filter(parentarticle=_article['id']).count()
        return info
        
    articles = map(_make_article_info, articles)

    paginator=PaginatorPro(articles,10)#分页器
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    
    try:
        articles=paginator.page(page)
    except (EmptyPage,InvalidPage):
        articles=paginator.page(paginator.num_pages)
    
    if paginator.num_pages>1: #控制'首页'和'尾页'标签的输出
        showFirstAndLast=True
    else:
        showFirstAndLast=False
    
    return render_to_response('blog_list.html',
                              {'articles':articles,
                               'articletypes':articletypes,
                               'toparticlelist':toparticlelist,
                               'topviewlist':topviewlist,
                               'showFirstAndLast':showFirstAndLast,
                               'recentcomments':recentcomments,},)

#文章分类列表主页面
def handletags(request,tags=''):
    try:
        articles = article.objects.filter(articletype__typename=tags).values('id','title','articletype__typename','publishdate','clicknums')#orm查询
    except Exception:
        raise Http404
    articletypes = articletypeList.objects.all()
    toparticlelist=article.objects.values('id','title').order_by('-publishdate')[0:5] #右边栏最新文章
    topviewlist = articles.order_by('clicknums')[0:10] #右边栏阅读排行
    recentcomments = comment.objects.values('username','usercomment','parentarticle__title','parentarticle__id').order_by('-publicdate')[0:5] #最新评论
    #将文章和所对应的评论表关联(获取评论数)
    def _make_article_info(_article):
        info = {}
        info['id'] = _article['id']
        info['title'] = _article['title']
        info['articletype__typename'] = _article['articletype__typename']
        info['publishdate'] = _article['publishdate']
        info['clicknums'] = _article['clicknums']
        info['commentnums'] = comment.objects.filter(parentarticle=_article['id']).count()
        return info
        
    articles = map(_make_article_info, articles)
    
    paginator=PaginatorPro(articles,10)#分页器
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    
    try:
        articles=paginator.page(page)
    except (EmptyPage,InvalidPage):
        articles=paginator.page(paginator.num_pages)
    
    if paginator.num_pages>1: #控制'首页'和'尾页'标签的输出
        showFirstAndLast=True
    else:
        showFirstAndLast=False
    
    return render_to_response('blog_typelist.html',
                              {'articles':articles,
                               'articletypes':articletypes,
                               'toparticlelist':toparticlelist,
                               'topviewlist':topviewlist,
                               'showFirstAndLast':showFirstAndLast,
                               'recentcomments':recentcomments},)

#文章显示页面
def handleblogcontent(request,id=''):
    try:
        blogobject = article.objects.get(id=id) #取出id对应的文章
    except Exception:
        raise Http404
    blogobject.clicknums += 1 #评论数+1
    blogobject.save()
    articletypes = articletypeList.objects.all() #文章分类
    articles = article.objects.values('id','title','clicknums')
    toparticlelist= articles.order_by('-publishdate')[0:5] #右边栏最新文章
    topviewlist = articles.order_by('clicknums')[0:10] #右边栏阅读排行
    recentcomments = comment.objects.values('username','usercomment','parentarticle__title','parentarticle__id').order_by('-publicdate')[0:5] #最新评论
    sameTypeArticle = articles.values('id','title').filter(articletype=blogobject.articletype).order_by('-publishdate') #取出和本文相同类型的文章(的id和title即可)
    sameTypeArticle=list(sameTypeArticle) #列表化
    index = sameTypeArticle.index({'id':blogobject.id,'title':blogobject.title}) #取出本文在相同文章列表中的位置
    if index > 0 : #不是第一篇文章
        preArticle = sameTypeArticle[index-1] #取出前一篇文章
    else:
        preArticle = False
        
    if index < len(sameTypeArticle)-1: #不是最后一篇文章
        nextArticle = sameTypeArticle[index+1]
    else:
        nextArticle =False
    #评论
    nodes = comment.objects.filter(parentarticle=id).all() #取出该文章id对应的评论
    #验证码
    verifyform = CaptchaForm()

    loginuser=None
    if request.siteuser: #取出登录的用户
        loginuser = UserInfo.objects.get(user_id=request.siteuser.id)
    
    if request.method == 'POST':
        if 'message' in request.POST and request.POST['message']: #提交评论
            message = request.POST['message']
            usrinfo = UserInfo.objects.get(user_id=request.siteuser.id)
            usrname = usrinfo.username
            usricon = usrinfo.avatar
            parentcomment = None
            if 'parent_id' in request.POST and request.POST['parent_id']:
                parent_id = request.POST['parent_id']
                parentcomment = comment.objects.get(id=parent_id)
            
            comment.objects.create(username=usrname,usericon=usricon,usercomment=message,
                                   parentarticle=article.objects.get(id=request.POST['article_id']),
                                   parent=parentcomment,)
            return HttpResponseRedirect(reverse('showArticle',args=id)+'#commentsarea') #防止重复提交
        
        if 'email' in request.POST and request.POST['email']: #提交登录
            def _login():
                email = request.POST.get('email', None)
                password = request.POST.get('password', None)
                if not email or not password:
                    raise RegisterLoginError("请输入邮箱和密码!")
                
                if not UserAuth.objects.filter(email=email, password=password).exists():
                    raise RegisterLoginError("无效的账户,请重新输入!")
                
                user = UserAuth.objects.get(email=email, password=password)
                return user
            try:
                user = _login()
                request.session['uid'] = user.user_id
                response = HttpResponseRedirect(reverse('showArticle',args=[id])+'#loginarea')
                response.set_cookie('username', user.user_id,)
                return response
            except RegisterLoginError as e:
                return render_to_response(
                    'blog_content.html',
                    {'blog':blogobject,
                    'articletypes':articletypes,
                    'toparticlelist':toparticlelist,
                    'topviewlist':topviewlist,
                    'preArticle':preArticle,
                    'nextArticle':nextArticle,
                    'nodes':nodes,'error_msg': e,},
                    context_instance=RequestContext(request)
                )
                
        if 'userlogout' in request.POST and request.POST['userlogout']: #退出
            try:
                del request.session['uid']
            except:
                pass
            finally:
                response = HttpResponseRedirect(reverse('showArticle',args=[id])+'#loginarea')
                response.delete_cookie('username')
                return response
        
        if 'registeremail' in request.POST and request.POST['registeremail']: #注册
            def _register(): #注册用户
                email = request.POST.get('registeremail', None)
                password = request.POST.get('registerpassword', None)
                username = request.POST.get('registernickname', None)
                if not email or not password:
                    raise RegisterLoginError("请输入邮箱和密码!")
                
                if UserAuth.objects.filter(email=email).exists():
                    raise RegisterLoginError("该邮箱已经被使用，请重新输入!")
                
                if not username:
                    raise RegisterLoginError("用户名不能为空!")
                usericon = None
                if 'inputfile' in request.FILES and request.FILES['inputfile']: #如果用户上传了头像
                    image = request.FILES['inputfile']
                    img = Image.open(image)
                    img.thumbnail((50,50),Image.ANTIALIAS)
                    name = os.path.splitext(image.name)[0]+ str(hash(time.time())) + os.path.splitext(image.name)[1] #初步防止文件名重复
                    usericon = '/media/usericons/'+name #用户头像的相对地址(用于前端显示)
                    pathname = os.path.join(settings.MEDIA_ROOT,'usericons',name) #用户目录的绝对地址(用于存储)
                    img.save(pathname)
                
                user = UserAuth.objects.create(email=email, password=password)
                if usericon:
                    UserInfo.objects.create(user_id=user.user_id, username=username,avatar=usericon)
                else:
                    UserInfo.objects.create(user_id=user.user_id, username=username)
                return user
              
            try:
                user = _register()
                request.session['uid'] = user.user_id
                response = HttpResponseRedirect(reverse('showArticle',args=[id])+'#loginarea')
                response.set_cookie('username', user.user_id,)
                return response
            except RegisterLoginError as e:
                return render_to_response(
                    'blog_content.html',
                    {'blog':blogobject,
                    'articletypes':articletypes,
                    'toparticlelist':toparticlelist,
                    'topviewlist':topviewlist,
                    'preArticle':preArticle,
                    'nextArticle':nextArticle,
                    'nodes':nodes,
                    'recentcomments':recentcomments,
                    'verifyform':verifyform,
                    'error_msg': e,},
                    context_instance=RequestContext(request)
                )

    return render_to_response('blog_content.html',
                              {'blog':blogobject,
                               'articletypes':articletypes,
                               'toparticlelist':toparticlelist,
                               'topviewlist':topviewlist,
                               'preArticle':preArticle,
                               'nextArticle':nextArticle,
                               'nodes':nodes,
                               'recentcomments':recentcomments,
                               'verifyform':verifyform,
                               'loginuser':loginuser,},
                              context_instance=RequestContext(request))

# 验证码ajax请求
@csrf_exempt
def handleverifycode(request):
    if request.method == 'POST':
        verifyform = CaptchaForm(request.POST)
        if not verifyform.is_valid():
            return HttpResponse('invalid')
        else:
            return HttpResponse('valid')
    else:
        verifyform = CaptchaForm()
        return HttpResponse(verifyform)

# 验证email是否已经注册
@csrf_exempt
def handleverifyemail(request):
    if request.method == 'POST':
        if 'email' in request.POST and request.POST['email']: #注册
            email = request.POST.get('email', None)
            if not email:
                return HttpResponse('Empty')
            if UserAuth.objects.filter(email=email).exists():
                return HttpResponse(False)
        return HttpResponse(True)

def handletest(request):
    return render_to_response('blog_main.html')

def login(request):
    print request.path
    print request.siteuser
    if request.siteuser:
        # already logged in
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'GET':
        return render_to_response(
            'login.html',
            context_instance=RequestContext(request)
        )
    
    def _login():
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            raise RegisterLoginError("Fill email and password")
        
        if not UserAuth.objects.filter(email=email, password=password).exists():
            raise RegisterLoginError("Invalid account")
        
        user = UserAuth.objects.get(email=email, password=password)
        return user
    
    try:
        user = _login()
        request.session['uid'] = user.user_id
        username = UserInfo.objects.get(user_id=user.user_id).username
        response = HttpResponseRedirect(reverse('home'))
        response.set_cookie('username', username, 3600,)
        return response
    except RegisterLoginError as e:
        return render_to_response(
            'login.html',
            {'error_msg': e},
            context_instance=RequestContext(request)
        )

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    finally:
        response = HttpResponseRedirect(reverse('home'))
        response.delete_cookie('username')
        return response

def login_error(request):
    return HttpResponse("OAuth Failure!")

def register(request):
    if request.method == 'GET':
        return render_to_response(
            'register.html', context_instance=RequestContext(request)
        )
    
    def _register():
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            raise RegisterLoginError("Fill email and password")
        
        if UserAuth.objects.filter(email=email).exists():
            raise RegisterLoginError("Email has been taken")
        
        user = UserAuth.objects.create(email=email, password=password)
        return user
    
    try:
        user = _register()
        request.session['uid'] = user.user_id
        return HttpResponseRedirect(reverse('register_step_2'))
    except RegisterLoginError as e:
        return render_to_response(
            'register.html',
            {'error_msg': e},
            context_instance=RequestContext(request)
        )

def register_step_2(request):
    if not request.siteuser:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'GET':
        return render_to_response(
            'register_step_2.html',
            {'email': UserAuth.objects.get(user_id=request.siteuser.id).email},
            context_instance=RequestContext(request)
        )
    
    def _register_step_2():
        username = request.POST.get('username', None)
        if not username:
            raise RegisterLoginError("Fill in username")
        
        UserInfo.objects.create(user_id=request.siteuser.id, username=username)
        
    try:
        _register_step_2()
        return HttpResponseRedirect(reverse('home'))
    except RegisterLoginError as e:
        return render_to_response(
            'register_step_2.html',
            {
                'email': UserAuth.objects.get(user_id=request.siteuser.id).email,
                'error_msg': e
            },
            context_instance=RequestContext(request)
        )


#分页类
class PaginatorPro(Paginator):
    def __init__(self, object_list, per_page, range_num=3, orphans=0,
                 allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page);
        self.range_num = range_num
    
    def page(self, number):
        self.page_num = number #当前页标
        return Paginator.page(self, number)
    
    def _get_page_range_pro(self):
        display_num = self.range_num * 2 + 1 #定义显示的分页总数
        if self.num_pages < display_num: #总页数小于定义显示的页数
            return Paginator._get_page_range(self) #直接调用父函数
        elif self.page_num < self.range_num:#当前页表距离首页距离小于range_num
            return range(1,display_num)
        elif self.num_pages-self.page_num < self.range_num: #当前页距离尾页的距离小于range_num
            return range(self.page_num-self.range_num+1,self.num_pages+1);
        else:
            return range(self.page_num-self.range_num+1,self.page_num+self.range_num+1)
    
    page_range_pro=property(_get_page_range_pro)