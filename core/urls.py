from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet, PublicEmployeeView, PublicEmployeeDetailView, PublicSingleEmployeeView, OrganizationDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/organization/<uuid:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('api/public/employees/<uuid:organization_id>/', PublicEmployeeView.as_view()),
    path('api/public/employee/<uuid:id>/', PublicEmployeeDetailView.as_view()),
    path('api/public/employee/<uuid:employee_id>/', PublicSingleEmployeeView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
