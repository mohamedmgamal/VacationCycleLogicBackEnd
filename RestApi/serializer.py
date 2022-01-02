from rest_framework import serializers
from RestApi import models
from RestApi.models import VacationRequests,Employee,OfficialVacations


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"

class VacationRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=VacationRequests
        fields=("vFrom" ,"vTo" ,"employeeID" ,"type" ,"status")

class UpdateRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=VacationRequests
        fields=("status",)


class RequestsSerializer(serializers.ModelSerializer):
    employeeName = serializers.CharField(source="employeeID.name", read_only=True)
    class Meta:
        model=VacationRequests
        fields="__all__"

class OfficialVacationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OfficialVacations
        fields="__all__"

class vacationsStatusSerializer(serializers.Serializer):
   numToken = serializers.IntegerField()
   numEarned = serializers.IntegerField()