from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('route/', views.route, name='route'),
    path('schadule/', views.schadule, name='schadule'),
    path('sayer/', views.sayer, name='sayer'),
    path('career/', views.career, name='career'),
    path('mission_and_vision/', views.mission_and_vision, name='mission_and_vision'),
    # path('test/', views.test, name='test'),
    path('load_data', views.load_data),
    path('get-end-points/<int:start_id>/', views.get_end_points, name='get_end_points'),
    path('get-schedules/<int:start_point_id>/<int:end_point_id>/', views.get_schedules, name='get_schedules'),
    path('bus-stops/', views.get_bus_stops, name='get_bus_stops'),
    path('temp_route_view', views.temp_route, name="route_view"),
    path('clear-history/', views.delete_history, name='clear_history')

]