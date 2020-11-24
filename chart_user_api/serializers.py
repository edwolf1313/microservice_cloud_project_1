from rest_framework import serializers
from chart_user_api.models import (
    chart_user_data
)

class ChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = chart_user_data
        fields ='__all__'

class CreateChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = chart_user_data
        fields ='__all__'

    def create(self, validated_data):
        chart = chart_user_data(**validated_data)
        chart.save()
        return chart
