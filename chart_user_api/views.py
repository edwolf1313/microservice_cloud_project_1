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
from django.conf import settings
import requests

class ChartAccessView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (JSONParser,)
    def get_object(self, pk,client_id):
        try:
            return chart_user_data.objects.get(pk=pk,client_id=client_id)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            if not (client_id := checkauth(request)):
                return Response(status.HTTP_403_FORBIDDEN)
            chartlist = chart_user_data.objects.all().filter(client_id=client_id)
            serializer = ChartSerializer(chartlist, many=True)
            return Response(serializer.data)
        except:
            return Response(status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            if not (client_id := checkauth(request)):
                return Response(status.HTTP_403_FORBIDDEN)
            request.data["client_id"] = client_id
            serializer = CreateChartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status.HTTP_204_NO_CONTENT)
        except:
            return Response(status.HTTP_403_FORBIDDEN)

    def put(self, request, id, format=None):
        #try:
            if not (client_id := checkauth(request)):
                return Response(status.HTTP_403_FORBIDDEN)
            chartlist = chart_user_data.objects.get(id=id,client_id=client_id)
            serializer = ChartSerializer(chartlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #except:
        #    return Response(status.HTTP_403_FORBIDDEN)

    def delete(self, request, chart_id, format=None):
        try:
            if not (client_id := checkauth(request)):
                return Response(status.HTTP_403_FORBIDDEN)
            chartproduct = self.get_object(chart_id,client_id)
            chartproduct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

def checkauth(request):
    import json
    try:
        auth_header_value = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header_value:
            req = requests.get(settings.SERVICE_API + "/authentication/auth/", timeout=10, headers={"Authorization":auth_header_value})
            if not req.status_code == 200:
                return 0
            return json.loads(req.text)['client_id']
        return 0
    except:
        return 0
