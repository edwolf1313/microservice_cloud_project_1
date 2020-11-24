from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chart_user_api.serializers import ChartSerializer, CreateChartSerializer

from chart_user_api.models import chart_user_data


class ChartAccessView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (JSONParser,)
    def get_object(self, pk):
        try:
            return chart_user_data.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, client_id, format=None):
        try:
            chartlist = chart_user_data.objects.all().filter(client_id=client_id)
            serializer = ChartSerializer(chartlist, many=True)
            return Response(serializer.data)
        except:
            return Response(status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            serializer = CreateChartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status.HTTP_204_NO_CONTENT)
        except:
            return Response(status.HTTP_403_FORBIDDEN)

    def put(self, request, id, client_id, format=None):
        chartlist = chart_user_data.objects.get(id=id,client_id=client_id)
        serializer = ChartSerializer(chartlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, chart_id, format=None):
        try:
            chartproduct = self.get_object(chart_id)
            chartproduct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
