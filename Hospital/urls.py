from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register_user),
    path('auth/login/', TokenObtainPairView.as_view()), # Still use library view for login [cite: 16]

    # Patients
    path('patients/', views.manage_patients),
    path('patients/<int:pk>/', views.patient_detail),

    # Doctors
    path('doctors/', views.manage_doctors),
    path('doctors/<int:pk>/', views.doctor_detail),

    # Mappings
    path('mappings/', views.manage_mappings),
    path('mappings/<int:pk>/', views.mapping_detail),
]