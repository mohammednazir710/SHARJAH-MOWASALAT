from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('route/', views.route, name='route'),
    path('schadule/', views.schadule, name='schadule'),
    path('test/', views.test, name='test')
]