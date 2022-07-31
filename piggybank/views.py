from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from piggybank.models import Transaction
from piggybank.serializers import CurrencySerializer
from piggybank.serializers import CategorySerializer
from piggybank.models import Category
from piggybank.models import Currency
from piggybank.serializers import TransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionModelViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
