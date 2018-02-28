from django.urls import path
from . import views



app_name = 'minerals'



urlpatterns = [
	path('', views.home, name="home"),
	path('detail/<int:id>/', views.detail, name="detail"),
	path('search/', views.search, name='search'),
    path('letter/<letter>/', views.letter, name='letter'),
    path('group/<group>/', views.group, name='group'),
    path('color/<color>/', views.color, name='color'),
]
