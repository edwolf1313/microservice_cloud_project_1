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
from decimal import *
from chart_user_api.models import chart_user_data
from django.conf import settings
import requests
import pprint
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
            chart_products = product_detail(serializer.data)

            return Response(chart_products)
        except:
            return Response(status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            if not (client_id := checkauth(request)):
                return Response(status.HTTP_403_FORBIDDEN)
            try:
                chart_data = chart_user_data.objects.get(product_id=request.data["product_id"],client_id=client_id)
                chart_instance = chart_data
                chart_data.quantity = int(chart_data.quantity) + int(request.data['quantity'])
                price = product_price(chart_data.product_id)
                chart_data.payment = int(chart_data.quantity) * int(Decimal(price))
                request.data['payment'] = chart_data.payment
                request.data['quantity'] = chart_data.quantity
                request.data['client_id'] = chart_data.client_id
                request.data['product_id'] = chart_data.product_id
                serializer = ChartSerializer(chart_instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                #print(serializer.errors)
                return Response(status.HTTP_400_BAD_REQUEST)
            except chart_user_data.DoesNotExist:
                request.data["client_id"] = client_id
                price = product_price(request.data["product_id"])
                request.data["payment"] = int(Decimal(price)) * int(request.data["quantity"])
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
            request.data["client_id"] = client_id
            price = product_price(request.data["product_id"])
            request.data["payment"] = int(Decimal(price)) * int(request.data["quantity"])
            serializer = ChartSerializer(chartlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_200_OK)
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

def product_price(product_id):
    try:
        req = requests.get(settings.PRODUCT_API + "/product_api/product-detail/{0}/".format(product_id), timeout=10)
        if not req.status_code == 200:
            return 0
        return req.json()['price']
    except:
        return 0

def product_detail(cart_products):
    for cart in cart_products:
        req = requests.get(settings.PRODUCT_API + "/product_api/product-detail/{0}/".format(cart['product_id']), timeout=10)
        cart['product_picture'] = req.json()['product_picture']
        cart['product_name'] = req.json()['name']
    return cart_products
