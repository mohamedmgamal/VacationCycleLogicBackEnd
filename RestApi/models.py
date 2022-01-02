from django.db import models

class Employee (models.Model):
    id  = models.AutoField(primary_key=True)
    name  = models.CharField(blank=False, null=False,max_length=24)
    hiringDate  = models.DateField(blank=False, null=False)
    profileImage =models.ImageField(upload_to='images/')
    jobtitle  = models.CharField(max_length=16,blank=False,null=True)
    birthdate = models.DateField(blank=False,null=False)
    mobileNo = models.CharField(max_length=16,blank=False,null=False)
    email = models.EmailField(blank=False,null=False)
    address = models.TextField(blank=False,null=False)
    def __str__(self):
        return f'{self.name}'


class OfficialVacations (models.Model):
    id = models.AutoField(primary_key=True)
    date =  models.DateField(blank=False, null=False)
    name = models.CharField(max_length=16,blank=False,null=False)
    def __str__(self):
        return f'{self.name}'

class VacationRequests (models.Model):
    Types_CHOICES = (
        ('annualVacation,', 'Annual Vacation,'),
        ('suddenVacation', 'Sudden Vacation'),
    )

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('disapprove', 'Disapprove'),
    )
    id = models.AutoField(primary_key=True)
    vFrom = models.DateField(blank=False, null=False)
    vTo = models.DateField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    employeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    numOfDays = models.IntegerField()
    type = models.CharField(max_length=15,
                              choices=Types_CHOICES)
    status = models.CharField(max_length=15,
                            choices=STATUS_CHOICES,
                            default='draft')

    def save(self, *args, **kwargs):
        self.numOfDays = (self.vTo - self.vFrom).days  + 1
        super(VacationRequests, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.employeeID.name} from : {self.vFrom} to : {self.vTo}'



