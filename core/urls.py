from django.contrib import admin
from django.urls import path

from piggybank import views
from piggybank.views import CurrencyListAPIView

from rest_framework import routers

router = routers.SimpleRouter()

router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('transactions', views.TransactionModelViewSet, basename='transaction')

urlpatterns = [
    path('currencies/', CurrencyListAPIView.as_view(), name='currency'),

    path('admin/', admin.site.urls),
] + router.urls
