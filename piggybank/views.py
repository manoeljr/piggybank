from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from piggybank.models import Transaction
from piggybank.permissions import IsAdminOrReadOnly
from piggybank.reports import transaction_reports
from piggybank.serializers import CurrencySerializer
from piggybank.serializers import CategorySerializer
from piggybank.models import Category
from piggybank.models import Currency
from piggybank.serializers import ReadTransactionSerializer
from piggybank.serializers import ReportEntrySerializer
from piggybank.serializers import ReportParamsSerializer
from piggybank.serializers import WriteTransactionSerializer


class CurrencyModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend, ]
    search_fields = ['description', ]
    ordering_fields = ['amount', 'date', ]
    filterset_fields = ['currency__code', ]

    def get_queryset(self):
        return Transaction.objects.select_related('currency', 'category', 'user').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer


class TransactionReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        params_serializer = ReportParamsSerializer(data=request.data, context={'request': request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()
        data = transaction_reports(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)
