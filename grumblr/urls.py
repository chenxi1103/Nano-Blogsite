"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from grumblr import views
from django.conf.urls import url
from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    )
from webapp import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^allPost', views.AllPost, name='allPost'),
    path('allPost',views.AllPost,name='allPost'),
    path('home',views.home, name='home'),
    path('login', LoginView.as_view(template_name='grumblr/login.html'), name='login'),
    path('logout', logout_then_login, name='logout'),
    path('register', views.register, name='register'),
    path('userProfile', views.showProfile,name='userProfile'),
    path('quickpost',views.qpost, name='quickpost'),
    path('editProfile', views.editProfile, name='editProfile'),
    path('checkUser',views.checkUser,name='checkUser'),
    path('followStream', views.followStream,name='followStream'),
    path('confirmEmail/<str:username>/<slug:token>/',views.confirmEmail, name = 'confirm'),
    url(r'^deletePost/(?P<id>\d+)$',views.deletePost, name='deletePost'),
    url(r'^deleteComment/(?P<id>\d+)$',views.deleteComment, name='deleteComment'),
    url(r'^get-changes/?$', views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', views.get_changes),
    url(r'^add-comments/(?P<id>\d+)$', views.add_comments,name='add_comments'),
    url(r'^get-comments/(?P<id>\d+)$', views.get_comments,name='get_comments'),
    url(r'^get-category/(?P<category>.+)$',views.get_category, name='get_category'),
    url(r'^get-followerStream', views.get_followerStream,name='get_followerStream'),
    url(r'^get-userPost', views.get_userPost,name='get_userPost'),
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
    url(r'^media/(?P<id>\d+)$',serve,{'document_root':settings.MEDIA_ROOT},name='picture'),
    url(r'^connection/(?P<operation>.+)/(?P<id>\d+)/$',views.followUser, name='followUser'),
    url(r'^category/(?P<category>.+)/$',views.checkByCategory, name='checkByCategory'),
    url(r'^user/post/', views.showProfile),
    url(r'^resetPassword/$', PasswordResetView.as_view(template_name='grumblr/password_reset.html'),name='reset_password'),
    url(r'^resetPassword/done/$',PasswordResetDoneView.as_view(template_name='grumblr/password_reset_done.html'),name='password_reset_done'),
    url(r'^resetPassword/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',PasswordResetConfirmView.as_view(template_name='grumblr/password_reset_confirm.html'),name='password_reset_confirm'),
    url(r'^resetPassword/complete/$',PasswordResetCompleteView.as_view(template_name='grumblr/password_reset_complete.html'),name='password_reset_complete'),
    path('changePassword', views.changePwd,name='changePwd'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)