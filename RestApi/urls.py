from django.urls import path


from . import  views
urlpatterns = [
    path('requestOfficialVacations/',views.requestOfficialVacations,),
    path('getOfficialVacations/',views.getOfficialVacations,)
    ,path('createEmployee/', views.createEmployee, name="createEmployee"),
    path('updateEmployee/<int:id>', views.updateEmployee, name="updateEmployee"),
    path('getEmployees/', views.getEmployees, name="getEmployees"),
    path('createRequest/',views.createRequest,name="createRequest"),
    path('updateRequest/<int:id>',views.updateRequest,name="updateRequest"),
    path('getRequests/',views.getRequests,name="getRequests"),
    path('getvacationsStatus/<int:id>',views.getvacationsStatus,name="getvacationsStatus")
]
