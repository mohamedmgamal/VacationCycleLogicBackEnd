from django.contrib import admin
from RestApi.models import Employee,OfficialVacations,VacationRequests
# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class OfficialVacationsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class VacationRequestsAdmin(admin.ModelAdmin):
    readonly_fields = ('id','numOfDays')
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(OfficialVacations,OfficialVacationsAdmin)
admin.site.register(VacationRequests,VacationRequestsAdmin)