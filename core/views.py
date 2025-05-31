from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveAPIView
from .models import Department, Employee, Organization
from .serializers import DepartmentSerializer, EmployeeSerializer, OrganizationTokenObtainPairSerializer, PublicEmployeeSerializer, OrganizationSerializer

class OrganizationTokenObtainPairView(TokenObtainPairView):
    serializer_class = OrganizationTokenObtainPairSerializer
    
class OrganizationDetailView(RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()  # 🔥 Add this line
    lookup_field = 'id'  # ✅ Optional if you're using UUIDs as primary keys

    def get_queryset(self):
        # Only filter if it's a list request
        if self.action == 'list':
            org_id = self.request.query_params.get('organization')
            if org_id:
                return Department.objects.filter(organization__id=org_id)
        return Department.objects.all()  # ✅ Allow retrieve/update to work

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Employee.objects.filter(organization=self.request.user)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user)
        
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PublicEmployeeSerializer
        return EmployeeSerializer

class PublicEmployeeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, organization_id):
        """
        Publicly fetch all employees under an organization.
        Used in Public ReactJS UI.
        """
        employees = Employee.objects.filter(organization__id=organization_id)
        serializer = PublicEmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
class PublicEmployeeDetailView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = PublicEmployeeSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
class PublicSingleEmployeeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
        serializer = PublicEmployeeSerializer(employee)
        return Response(serializer.data)

# TEST