from datetime import date

from django.contrib.auth.models import User
from rest_framework import serializers

from piggybank.models import Category
from piggybank.models import Currency
from piggybank.models import Transaction


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = fields


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']


class WriteTransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    currency = serializers.SlugRelatedField(slug_field='code', queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'currency', 'date', 'description', 'category']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['category'].queryset = user.categories.all()


class ReadTransactionSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer()
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'currency', 'date', 'description', 'category', 'user']
        read_only_fields = fields


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class PersonSerializer(serializers.Serializer):
    """
    Classes desenvolvida para teste de como funciona um serializer,
    não faz parte do desenvolvimento das transactions
    """
    first_name = serializers.CharField(allow_null=True)
    birthdate = serializers.DateField()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        """ Pegando a variavel age e modificando subescrevando o metodo built-in """
        delta = date.today() - obj.birthdate
        return int(delta.days / 365)

    def validate_birthdate(self, value):
        """ Sobescrevendo o metodo de validação do DRF, is_valid() """
        if value > date.today():
            raise serializers.ValidationError('The birthdate must be a date before today.')
        return value

    def validate(self, data):
        """ Verificando se o campo first_name está vazio """
        if not data['first_name']:
            raise serializers.ValidationError('You must inform either the first name.')
        return data
