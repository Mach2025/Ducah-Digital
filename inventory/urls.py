from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,SaleViewSet,DashboardAPIView, PaymentViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'payments', PaymentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/',DashboardAPIView.as_view(), name='dashboard')
    

]