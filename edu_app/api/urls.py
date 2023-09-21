from django.urls import path
from . import views

urlpatterns = [
    path('lessons/list/', views.LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/product/<int:product_id>/', views.ProductLessonListAPIView.as_view(), name='product-lesson-list'),
    path('product/stats/', views.ProductStatsAPIView.as_view(), name='product-stats'),
]
