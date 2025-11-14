from django.urls import path
from . import views

urlpatterns = [
    path('detect/', views.detectAIgeneratedImage, name='detectAIgeneratedImage'),
]
