from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'apps'
urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('echarts1/', views.echarts1, name='echarts1'),
    path('echarts2/', views.echarts2, name='echarts2'),
    path('person_info/', views.person_info, name='person_info'),
    path('safe_setting/', views.safe_setting, name='safe_setting'),
    path('bh_list/', views.bh_list, name='bh_list'),
    path('line_chart/', views.line_chart, name='line_chart'),
    path('pie_chart/', views.pie_chart, name='pie_chart'),
    path('uploadImg/', views.uploadImg, name='uploadImg'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
