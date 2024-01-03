from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    path('createroom/',views.createroom, name = 'createroom'),
    path('updateroom/<str:pk>/',views.updateroom, name = 'updateroom'),
    path('deleteroom/<str:pk>/',views.deleteroom, name = 'deleteroom'),
    path('login/',views.loginpage, name = 'login'),
    path('logout/',views.logoutpage, name = 'logout'),
    path('register/',views.registerpage, name = 'register'),
    path('delete-message/<str:pk>/',views.deletemessage, name = 'delete-message'),
    path('profile/<str:pk>/', views.userprofile, name = 'userprofile'),
    path('update-user/', views.updateuser, name = 'updateuser'),
    path('topics/', views.topicspage, name = 'topics'),
    path('activitypage/', views.activitypage, name = 'activity')
]
