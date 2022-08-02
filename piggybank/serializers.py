from django.contrib.auth.models import User
from rest_framework import serializers

from piggybank.models import Category
from piggybank.models import Currency
from piggybank.models import Transaction


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class WriteTransactionSerializer(serializers.ModelSerializer):

    currency = serializers.SlugRelatedField(slug_field='code', queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = ['amount', 'currency', 'date', 'description', 'category']


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = fields


class ReadTransactionSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer()
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'currency', 'date', 'description', 'category', 'user']
        read_only_fields = fields