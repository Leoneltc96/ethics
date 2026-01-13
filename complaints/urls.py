from django.urls import path
from . import views

urlpatterns = [
    path('testAI/', views.testAI),
    path('get_complaint/', views.get_complaint),
    path('save_complaint/', views.save_complaint)

]
