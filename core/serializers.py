from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Department, Employee, Organization

class OrganizationTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['org_id'] = str(user.id)
        return token
    
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'logo']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class PublicEmployeeSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    organization = serializers.UUIDField(source='organization.id')
    profile_pic = serializers.ImageField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'profile_pic',
            'name',
            'contact_no',
            'blood_group',
            'email',
            'short_intro',
            'designation',
            'linkedin_url',
            'department',
            'organization',
        ]
