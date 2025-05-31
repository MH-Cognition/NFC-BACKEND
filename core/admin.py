from django.contrib import admin
from django import forms
from .models import Organization, Department, Employee

class OrganizationCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationCreationForm
    list_display = ('username', 'name', 'id')
    fields = ('name', 'username', 'password')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')

# ✅ Add custom EmployeeAdmin with filter
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department', 'organization', 'email')
    list_filter = ('organization',)  # Adds filter sidebar for organization
    search_fields = ('name', 'email', 'designation')  # Optional: makes admin searchable
