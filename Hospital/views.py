from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer

#  AUTHENTICATION 

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PATIENT MANAGEMENT 

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_patients(request):
    if request.method == 'GET':
        # Retrieve all patients 
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # Add a new patient linked to the user 
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'GET': 
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    if request.method == 'PUT': 
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE': 
        patient.delete()
        return Response({"message": "Patient deleted"}, status=status.HTTP_204_NO_CONTENT)

# DOCTOR MANAGEMENT 

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_doctors(request):
    if request.method == 'GET': 
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    if request.method == 'POST': 
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'GET': 
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    if request.method == 'PUT': 
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE': 
        doctor.delete()
        return Response({"message": "Doctor deleted"}, status=status.HTTP_204_NO_CONTENT)

# MAPPING MANAGEMENT 

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_mappings(request):
    if request.method == 'GET': 
        mappings = PatientDoctorMapping.objects.all()
        serializer = MappingSerializer(mappings, many=True)
        return Response(serializer.data)

    if request.method == 'POST': 
        serializer = MappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def mapping_detail(request, pk):
    if request.method == 'GET': 
        # Get all doctors assigned to a specific patient
        patient = get_object_or_404(Patient, pk=pk)
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = MappingSerializer(mappings, many=True)
        return Response(serializer.data)

    if request.method == 'DELETE': 
        # Delete a specific mapping by mapping ID
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        mapping.delete()
        return Response({"message": "Mapping deleted"}, status=status.HTTP_204_NO_CONTENT)