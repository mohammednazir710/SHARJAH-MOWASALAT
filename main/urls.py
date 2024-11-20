from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('route/', views.route, name='route'),
    path('schadule/', views.schadule, name='schadule'),
    path('test/', views.test, name='test'),
    path('load_data', views.load_location_data),
    path('get-end-points/<str:start_code>/', views.get_end_points, name='get_end_points'),
    path('get-schedules/<str:start_point_code>/<str:end_point_code>/', views.get_schedules, name='get_schedules'),
    path('api/bus-stops/', views.get_bus_stops, name='get_bus_stops'),
    path('temp_route_view', views.temp_route)

]