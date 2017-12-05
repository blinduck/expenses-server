from rest_framework import serializers
from ..models import Record, MasterBudget, Category


class RecordCreateSerializer(serializers.ModelSerializer):
    masterbudget = serializers.PrimaryKeyRelatedField(
        queryset=MasterBudget.objects.all(), allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, allow_empty=True, queryset=Category.objects.all())

    class Meta:
        model = Record
        fields = ('id', 'user', 'household', 'categories', 'amount', 'name', 'type', 'masterbudget', 'time')


class RecordListSerializer(serializers.ModelSerializer):
    
    masterbudget = serializers.StringRelatedField(read_only=True)
    budget = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields =  "__all__"

    categories = CategorySerializer(many=True, read_only=True, )

    class Meta:
        model = Record
        fields = ('id', 'user', 'household', 'categories',
                  'amount', 'name', 'type',
                  'masterbudget', 'budget', 'time')
