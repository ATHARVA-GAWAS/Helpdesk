"""
URL configuration for FBhelpdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
     # URLs for user registration and authentication
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),

    path('create-facebook-page/', views.create_facebook_page, name='create_facebook_page'),
    # URLs for managing Facebook Page connections
    path('fbpageconnections/', views.fb_page_connections, name='fb_page_connections'),
    path('fb-page/connections/<int:fb_page_id>/delete/', views.delete_fb_page, name='delete_fb_page'),

    # URLs for viewing conversations and replying to messages
    path('conversations/', views.view_conversations, name='view_conversations'),
    path('conversations/<int:conversation_id>/reply/', views.reply_to_message, name='reply_to_message'),
]


