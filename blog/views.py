#coding=utf-8
from django.shortcuts import render_to_response
from blog.models import article, articletypeList, comment
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http.response import Http404, HttpResponse
from django.template.context import RequestContext
from PIL import Image


# as same as SiteUser, import the following two just for this example
# to get the siet_name_zh
from socialoauth import SocialSites
from myblog.settings import SOCIALOAUTH_SITES
from socialoauth.exception import SocialAPIError
from myblog import settings
import os
import time
from blog.forms import CaptchaForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import re

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
    articles = article.objects.values('id','title','articletype__typename','publishdate','istop','clicknums','commentnums')
    # =======================右边栏显示============================
    articletypes = articletypeList.objects.all().order_by('typename')
    toparticlelist=articles.order_by('-publishdate')[0:5] #右边栏最新文章
    topviewlist = articles.order_by('-clicknums')[0:10] #右边栏阅读排行
    topcommentlist = articles.order_by('-commentnums')[0:5] #右边栏评论排行
    recentcomments = comment.objects.values('username','usercomment','parentarticle__title','parentarticle__id').order_by('-publicdate')[0:5] #最新评论
    # ==========================================================
    articles = articles.order_by('-istop','-publishdate') #按照置顶和时间排序
    
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
                               'topcommentlist':topcommentlist,
                               'showFirstAndLast':showFirstAndLast,
                               'recentcomments':recentcomments,},)

#文章分类列表主页面
def handletags(request,tags=''):
    try:
        articles = article.objects.filter(articletype__typename=tags).values('id','title','articletype__typename','publishdate','clicknums','commentnums')#orm查询
    except Exception:
        raise Http404
    # =======================右边栏显示============================
    articletypes = articletypeList.objects.all().order_by('typename')
    allarticles = article.objects.values('id','title','publishdate','clicknums','commentnums') #取出所有文章id和title
    toparticlelist= allarticles.order_by('-publishdate')[0:5] #右边栏最新文章
    topviewlist = allarticles.order_by('-clicknums')[0:10] #右边栏阅读排行
    topcommentlist = allarticles.order_by('-commentnums')[0:5] #右边栏评论排行
    recentcomments = comment.objects.values('username','usercomment','parentarticle__title','parentarticle__id').order_by('-publicdate')[0:5] #最新评论
    # ==========================================================
    articles = articles.order_by('-publishdate')    
    
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
                               'topcommentlist':topcommentlist,
                               'showFirstAndLast':showFirstAndLast,
                               'recentcomments':recentcomments},)

#文章显示页面
def handleblogcontent(request,id=''):
    try:
        blogobject = article.objects.get(id=id) #取出id对应的文章
    except Exception:
        raise Http404
    # =======================右边栏显示============================
    articletypes = articletypeList.objects.all() #文章分类
    articles = article.objects.values('id','title','clicknums','commentnums')
    toparticlelist= articles.order_by('-publishdate')[0:5] #右边栏最新文章
    topviewlist = articles.order_by('-clicknums')[0:10] #右边栏阅读排行
    topcommentlist = articles.order_by('-commentnums')[0:5] #右边栏评论排行
    recentcomments = comment.objects.values('username','usercomment','parentarticle__title','parentarticle__id').order_by('-publicdate')[0:5] #最新评论
    # ==========================================================
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
    
    blogobject.clicknums += 1 #浏览数+1
    blogobject.save()
    return render_to_response('blog_content.html',
                              {'blog':blogobject,
                               'articletypes':articletypes,
                               'toparticlelist':toparticlelist,
                               'topviewlist':topviewlist,
                               'topcommentlist':topcommentlist,
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

# 异步提交评论
@csrf_exempt
def postcomment(request):
    if request.method == 'POST':
        if 'message' in request.POST and request.POST['message'] and request.POST['user_id']: #提交评论
            message = request.POST['message']
            message = re.sub(r'\<', r'&lt;', message) #正则处理表情,换行等
            message = re.sub(r'\>', r'&gt;', message)
            message = re.sub(r'\n', r'<br/>', message)
            message = re.sub(r'\[em_([0-9]*)\]', r'<img src="/static/img/qqface/\1.gif" border="0" />', message)
            usrinfo = UserInfo.objects.get(user_id=request.POST['user_id'])
            usrname = usrinfo.username
            usricon = usrinfo.avatar
            parentarticleId = request.POST['article_id']
            parentcomment = None
            if 'parent_id' in request.POST and request.POST['parent_id']:
                parent_id = request.POST['parent_id']
                parentcomment = comment.objects.get(id=parent_id)
            
            currentcomment = comment.objects.create(username=usrname,usericon=usricon,usercomment=message,
                                   parentarticle=article.objects.get(id=parentarticleId),parent=parentcomment,)
            blogobject = article.objects.get(id=parentarticleId)
            blogobject.commentnums += 1 #评论数+1
            blogobject.save()
            return render_to_response('comment.html',{'node':currentcomment},context_instance=RequestContext(request))
    pass

@csrf_exempt
def login(request):
    if request.method == 'POST':
        if 'email' in request.POST and request.POST['email']: #提交登录(本地用户)
            def _login():
                email = request.POST.get('email', None)
                password = request.POST.get('password', None)
                if not email or not password:
                    raise RegisterLoginError("1") #请输入邮箱和密码!
                
                if not UserAuth.objects.filter(email=email).exists():
                    raise RegisterLoginError("2") #无效的账户,请重新输入!
                
                user = UserAuth.objects.get(email=email)
                if not check_password(password,user.password):
                    raise RegisterLoginError("3") #密码错误!
                return user
            try:
                user = _login()
                request.session['uid'] = user.user_id
                loginuser = UserInfo.objects.get(user_id=user.user_id)
                request_from =  request.META.get('HTTP_REFERER',"/").split('/')
                length = len(request_from)
                return render_to_response('login.html',
                                          {'loginuser':loginuser,'blog_id':request_from[length-2]},
                                          context_instance=RequestContext(request))
            except RegisterLoginError as e:
                return HttpResponse(e)
        
@csrf_exempt
def logout(request):
    try:
        del request.session['uid']
        response = render_to_response('logout.html',context_instance=RequestContext(request))
    except:
        response = HttpResponse('logoutfail')
    finally:
        return response

@csrf_exempt
def register(request):
    if request.method == 'POST':
        if 'registeremail' in request.POST and request.POST['registeremail']: #注册
            def _register(): #注册用户
                email = request.POST.get('registeremail', None)
                password = request.POST.get('registerpassword', None)
                username = request.POST.get('registernickname', None)
                if not email or not password:
                    raise RegisterLoginError("1") #请输入邮箱和密码!
                
                if UserAuth.objects.filter(email=email).exists():
                    raise RegisterLoginError("2") #该邮箱已经被使用，请重新输入!
                
                if not username:
                    raise RegisterLoginError("3") #用户名不能为空!
                usericon = None
                if 'inputfile' in request.FILES and request.FILES['inputfile']: #如果用户上传了头像
                    image = request.FILES['inputfile']
                    img = Image.open(image)
                    img.thumbnail((50,50),Image.ANTIALIAS)
                    name = os.path.splitext(image.name)[0]+ str(hash(time.time())) + os.path.splitext(image.name)[1] #初步防止文件名重复
                    usericon = '/media/usericons/'+name #用户头像的相对地址(用于前端显示)
                    pathname = os.path.join(settings.MEDIA_ROOT,'usericons',name) #用户目录的绝对地址(用于存储)
                    img.save(pathname)
                password = make_password(password,None,'pbkdf2_sha256')
                user = UserAuth.objects.create(email=email, password=password)
                if usericon:
                    UserInfo.objects.create(user_id=user.user_id, username=username,avatar=usericon)
                else:
                    UserInfo.objects.create(user_id=user.user_id, username=username)
                return user
              
            try:
                user = _register()
                request.session['uid'] = user.user_id
                loginuser = UserInfo.objects.get(user_id=user.user_id)
                request_from =  request.META.get('HTTP_REFERER',"/").split('/')
                length = len(request_from)
                return render_to_response('login.html',
                                          {'loginuser':loginuser,'blog_id':request_from[length-2]},
                                          context_instance=RequestContext(request))
            except RegisterLoginError as e:
                return HttpResponse(e)
    pass

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