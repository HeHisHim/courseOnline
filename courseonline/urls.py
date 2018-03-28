"""courseonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve
from django.conf.urls.static import static

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, IndexView
from courseonline.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL
from users.views import page_error, page_not_found
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    path('reset/<active_code>/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # 课程机构url配置
    path('org/', include('organization.urls', namespace="org")),

    # 课程相关url配置
    path('course/', include('courses.urls', namespace="course")),

    # 个人信息相关url配置
    path('users/', include('users.urls', namespace="users")),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)  # 配置图片上传函数

# urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

# 全局404页面配置
handler404 = page_not_found

# 全局500页面配置
handler500 = page_error
