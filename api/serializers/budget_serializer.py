from rest_framework import serializers
from ..models import Budget, Record



class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('remainder', 'start_time', 'end_time')


class BudgetWithRecordsSeralizer(serializers.ModelSerializer):
    class RecordSerializer(serializers.ModelSerializer):
        class Meta:
            model= Record
            fields = '__all__'

    records = RecordSerializer(source='record_set', many=True, read_only=True)
    masterbudget = serializers.StringRelatedField(read_only=True)

    class Meta:
        model= Budget
        fields = '__all__'
