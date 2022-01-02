from datetime import timedelta, date, datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

from RestApi.models import OfficialVacations, Employee , VacationRequests
from RestApi.serializer import EmployeeSerializer, VacationRequestsSerializer, OfficialVacationsSerializer, \
    RequestsSerializer, UpdateRequestsSerializer ,vacationsStatusSerializer


@api_view(["GET"])
def requestOfficialVacations(request):
    r = requests.get('https://holidayapi.com/v1/holidays?pretty&key=8534a5ae-511c-4895-8e2e-28f14a5fe3bd&country=EG&year=2021')
    if r.status_code == 200:
        for holiday in r.json()['holidays']:
            OfficialVacations(date=holiday['date'],name=holiday['name']).save()
        return Response(data={
            "success": True,
            "message": "Official Vacations fetched successfully "
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        "success": False,
        "errors":"cant fetch Official Vacations"
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def createEmployee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success": True,
            "message": "New employee added Successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def updateEmployee(request,id):
    serializer = EmployeeSerializer(Employee.objects.get(pk=id), data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "Success": True
            , "Massage": "Employee updated"
        }, status=status.HTTP_200_OK)
    return Response(data={
        "Success": False
        , "Error": serializer.errors
    })
@api_view(["GET"])
def getEmployees(request):
    employees = Employee.objects.all()
    response = EmployeeSerializer(instance=employees, many=True)
    return Response(data=response.data, status=status.HTTP_200_OK)
@api_view(["POST"])
def createRequest(request):
    serializer = VacationRequestsSerializer(data=request.data)
    if serializer.is_valid() :
        if (getTakenVacations(request.data['employeeID'])>=getallowedVacations(request.data['employeeID'])):
            return Response(data={
                "success": False,
                "errors": "You have exceeded the maximum vacation limit"
            }, status=status.HTTP_400_BAD_REQUEST)

        if haveOfficialVacations(request.data['vFrom'], request.data['vTo']):
            return Response(data={
                "success": False,
                "errors": "Can't create vacation requests that overlaps official vacations"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={
            "success": True,
            "message": "New request added Successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def updateRequest(request,id):
    serializer = UpdateRequestsSerializer(VacationRequests.objects.get(pk=id), data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "Success": True
            , "Massage": "Request updated"
        }, status=status.HTTP_200_OK)
    return Response(data={
        "Success": False
        , "Error": serializer.errors
    })
@api_view(["GET"])
def getRequests(request):
    requests = VacationRequests.objects.all()
    response = RequestsSerializer(instance=requests, many=True)
    return Response(data=response.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def getvacationsStatus(request,id):
        yourdata= {"numToken":  getTakenVacations(id), "numEarned": getallowedVacations(id) }
        results = vacationsStatusSerializer(yourdata, many=False).data
        return Response(data=results, status=status.HTTP_200_OK)
def getTakenVacations(empId):
    Vacs = VacationRequests.objects.filter(employeeID__id=empId).filter(status='approved')
    totalDays = 0
    for vac in  Vacs :
        totalDays += vac.numOfDays
    return totalDays

def getallowedVacations(empId):
    emp = Employee.objects.get(pk=empId)
    numOfYears = (date.today() - emp.hiringDate ).days  // 365.2422
    if numOfYears > 10:
        return 30
    else:
        return 21

def haveOfficialVacations (vFrom,vTo):
    vFrom =  datetime.strptime(vFrom, "%Y-%m-%d").date()
    vTo =  datetime.strptime(vTo, "%Y-%m-%d").date()
    if not vFrom==vTo:
        for i in range((vTo - vFrom).days + 1):
            if OfficialVacations.objects.filter(date=vFrom + timedelta(days=i)) :
                return True
        return False
    else:
        if (OfficialVacations.objects.filter(date=vFrom)):
                return True
        return False

@api_view(["GET"])
def getOfficialVacations(request):
    vcs = OfficialVacations.objects.all()
    response = OfficialVacationsSerializer(instance=vcs, many=True)
    return Response(data=response.data, status=status.HTTP_200_OK)