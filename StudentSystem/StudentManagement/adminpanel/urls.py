from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.handlelogin, name='login'),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.handlelogout, name='logout'),
    path('addstudent/', views.addstudent, name='addstudent'),
    path('showstudents/', views.showstudents, name='showstudents'),
    path('getstudent/', views.getstudent, name='getstudent'),
    path('deletestudent/<sid>', views.deletestudent, name='deletestudent'),
    path('updatestudent/<sid>', views.updatestudent, name='update'),
]
