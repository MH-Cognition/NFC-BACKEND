"""
URL configuration for digital_portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    DepartmentViewSet,
    EmployeeViewSet,
    PublicEmployeeView,
    OrganizationTokenObtainPairView,
    PublicEmployeeDetailView,
    PublicSingleEmployeeView,
    OrganizationDetailView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/organization/<uuid:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('api/public/employees/<uuid:organization_id>/', PublicEmployeeView.as_view()),
    path('api/public/employee/<uuid:id>/', PublicEmployeeDetailView.as_view()),
    path('api/public/employee/<uuid:employee_id>/', PublicSingleEmployeeView.as_view()),
    path('api/token/', OrganizationTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
