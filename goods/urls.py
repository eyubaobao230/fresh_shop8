from django.urls import path

from goods import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/<int:id>/', views.detail, name='detail'),
]