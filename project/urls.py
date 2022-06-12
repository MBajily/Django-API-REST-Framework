"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from tickets import views
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('from_models/', views.no_rest_from_model),
    path('rest/fbv/', views.FBV_List),
    path('rest/fbv/<int:pk>', views.FBV_pk),
    path('rest/cbv/', views.CBV_List.as_view()),
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),
    path('rest/mixins/', views.mixins_list.as_view()),
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),
    path('rest/generics/', views.generics_list.as_view()),
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    path('rest/viewsets/', include(router.urls)),
    path('fbv/find_movie/', views.find_movie),
    path('fbv/new_reservation/', views.new_reservation),

    path('api-auth', include('rest_framework.urls')),

    # Token authentication
    path('api-token-auth', obtain_auth_token),

    # Post pk generics Post_pk
    path('post/generics/<int:pk>', views.Post_pk.as_view()),
]
