from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from .models import Product,Sale, Payment
from .serializers import ProductSerializer,SaleSerializer, PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum,F


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer    

class DashboardAPIView(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        total_sales = Sale.objects.count()
        today_revenue = Sale.objects.aggregate(
    total=Sum('total_amount')
)['total'] or 0
        low_stock_products = Product.objects.filter(
            quantity__lte=F('reorder_level')
        ).count()

        return Response({
            'message': 'Welcome to Ducah Digital',
            'total_products': total_products,
            'total_sales': total_sales,
            'today_revenue': today_revenue,
            'low_stock_products': low_stock_products
        })
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
     
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save()

        if payment.status == "Paid":
            message = "Payment recorded successfully."

        elif payment.status == "Pending":
            message = "  Payment is awaiting confirmation."

        else:
            message = " Payment failed. No money was received."

        return Response(
            {
                "message": message,
                "payment": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
