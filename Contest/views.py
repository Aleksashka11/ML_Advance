from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import F, ExpressionWrapper, FloatField
from rest_framework import generics, filters

from EmployeeApp.models import Departments, Employees, Liquids, Analysis
from EmployeeApp.serializers import DepartmentsSerializer, EmployeesSerializer, LiquidsConcentrationSerializer, EmployeeNameSerializer, LiquidsPeriodSerializer


class EmployeesAPIView(generics.ListCreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    search_fields = ['EmployeeName']
    filter_backends = (filters.SearchFilter,)

@csrf_exempt
def departmentApi(request,id=0):
    if request.method=='GET':
        departments = Departments.objects.all()
        departments_serializer = DepartmentsSerializer(departments,many=True)
        return JsonResponse(departments_serializer.data, safe=False)
    elif request.method=='POST':
        department_data = JSONParser().parse(request)
        departments_serializer = DepartmentsSerializer(data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method=='PUT':
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        departments_serializer = DepartmentsSerializer(department, data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to update successfully", safe=False)
    elif request.method=='DELETE':
        department = Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def employeeApi(request,id=0):
    if request.method=='GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeesSerializer(employees,many=True)
        return JsonResponse(employees_serializer.data, safe=False)
    elif request.method=='POST':
        employee_data = JSONParser().parse(request)
        employees_serializer = EmployeesSerializer(data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method=='PUT':
        employee_data = JSONParser().parse(request)
        employee = Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
        employees_serializer = EmployeesSerializer(employee, data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to update successfully", safe=False)
    elif request.method=='DELETE':
        employee = Employees.objects.get(EmployeeId=id)
        employee.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def getConcentration(request):
    if request.method=="GET":
        query = Liquids.objects.filter(LiquidEmployeeId=1).annotate(concentration=ExpressionWrapper(F('DetectedMass')  * 1.0  / F('TakenMass'), output_field=FloatField()))
        query_serializer = LiquidsConcentrationSerializer(query,many=True)
        return JsonResponse(query_serializer.data, safe=False)

@csrf_exempt
def filterByAnalysis(request):
    if request.method=="GET":
        query = Employees.objects.values('EmployeeId', 'EmployeeName').filter(analysis__AnalysisType='Saliva')
        query_serializer = EmployeeNameSerializer(query,many=True)
        return JsonResponse(query_serializer.data, safe=False)

@csrf_exempt
def getPeriod(request):
    if request.method=="GET":
        query = Liquids.objects.filter(LiquidEmployeeId=1).annotate(period=ExpressionWrapper((F('DetectedMass')  * 1.0  / F('TakenMass')) / 0.1, output_field=FloatField()))
        query_serializer = LiquidsPeriodSerializer(query,many=True)
        return JsonResponse(query_serializer.data, safe=False)





# Create your views here.
