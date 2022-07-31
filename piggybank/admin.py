from django.contrib import admin

from piggybank.models import Category
from piggybank.models import Currency
from piggybank.models import Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'currency', 'date', 'description', 'category']
