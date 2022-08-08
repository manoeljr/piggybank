from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from piggybank import views
from piggybank.views import CurrencyListAPIView

from rest_framework import routers

router = routers.SimpleRouter()

router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('transactions', views.TransactionModelViewSet, basename='transaction')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token, name='obtain-auth-token'),

    path('currencies/', CurrencyListAPIView.as_view(), name='currency'),
    path('report/', views.TransactionReportAPIView.as_view(), name='report'),
    path('admin/', admin.site.urls),
] + router.urls
