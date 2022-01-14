from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('',views.reg,name='reg'),
    path('login/',views.log,name='log'),
    path('logout/',views.log_out,name='log_out'),
    path('create/',views.create,name='create'),
    path('show/',views.show,name='show'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('download/<int:id>',views.download,name='download')

]
