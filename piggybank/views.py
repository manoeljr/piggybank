from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from piggybank.models import Transaction
from piggybank.serializers import CurrencySerializer
from piggybank.serializers import CategorySerializer
from piggybank.models import Category
from piggybank.models import Currency
from piggybank.serializers import ReadTransactionSerializer
from piggybank.serializers import WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend,]
    search_fields = ['description',]
    ordering_fields = ['amount', 'date',]
    filterset_fields = ['currency__code',]

    def get_queryset(self):
        return Transaction.objects.select_related('currency', 'category', 'user').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer