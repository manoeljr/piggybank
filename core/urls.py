import debug_toolbar
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from piggybank import views

from rest_framework import routers

router = routers.SimpleRouter()

router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('transactions', views.TransactionModelViewSet, basename='transaction')
router.register('currencies', views.CurrencyModelViewSet, basename='currency')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token, name='obtain-auth-token'),

    path('report/', views.TransactionReportAPIView.as_view(), name='report'),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
] + router.urls
