import datetime
from dataclasses import dataclass
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Sum

from piggybank.models import Category
from piggybank.models import Transaction

@dataclass
class ReportEntry:
    category: Category
    total: Decimal
    count: int
    avg: Decimal

@dataclass
class ReportParams:
    start_date: datetime.datetime
    end_date: datetime.datetime
    user: User

def transaction_reports(params: ReportParams):
    data = []
    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date_lte=params.end_date
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount')
    )
    categories_index = {}
    for category in Category.objects.all():
        categories_index[category.pk] = category

    for entry in queryset:
        category = categories_index.get(entry['category'])
        report_entry = ReportEntry(category, entry['total'], entry['count'], entry['avg'])
        data.append(report_entry)

    return data