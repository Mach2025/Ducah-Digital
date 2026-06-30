from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from .models import Product,Sale
from .serializers import ProductSerializer,SaleSerializer
from rest_framework import APIView
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer    

class DashboardView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to Ducah Digital'})
