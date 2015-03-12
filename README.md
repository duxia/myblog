# SweetCoffee's Blog

### 博客地址：http://www.sweetcoffee.tk

该版本为本地调试的版本，未加入最终上线版本的qq登录功能，其他功能基本一致

### 版本及需求说明
*	django == 1.7.3
*	django-admin-bootstrapped == 2.3.2
*	django-ckeditor == 4.4.7
*	Pillow == 2.7.0
*	django-mptt == 0.6.1
*	socialoauth == 0.3.3
*	django-social-login == 0.2.0
*	six == 1.9.0
*	django-simple-captcha == 0.4.4

以上均是必要的依赖(pip请自行安装)，安装完成后才能正常开启本地运行模式，例如：
```bash
pip install django==1.7.3
pip install django-admin-bootstrapped==2.3.2
...
```
使用方法：
```bash
cd myblog
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
浏览器进入http://127.0.0.1:8000
```

