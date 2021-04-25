from django.db import models

# Create your models here.
class approvals(models.Model):
    DEPENDANT_CHOICES=(
        ('0','0'),
        ('1','1'),
        ('2','2'),
        ('3','3+') 
    )
    GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female')
    )
    MARRIED_CHOICES=(
        ('Yes','Yes'),
        ('No','No')
    )
    GRADUATED_CHOICES=(
        ('Graduate','Graduated'),
        ('Not_Graduate','Not_Graduate')
    )
    SELFEMPLOYED_CHOICES=(
        ('Yes','Yes'),
        ('No','No')
    )
    PROPERTY_CHOICES=(
        ('Rural','Rural'),
        ('Semiurban','Semiurban'),
        ('Urban','Urban')
    )

    dependants=models.CharField(max_length=15,choices=DEPENDANT_CHOICES)
    applicantincome=models.IntegerField(default=0)
    coapplicantincome=models.IntegerField(default=0)
    loanamt=models.IntegerField(default=0)
    loanterm=models.IntegerField(default=0)
    credithistory=models.IntegerField(default=0)
    gender=models.CharField(max_length=15,choices=GENDER_CHOICES)
    married=models.CharField(max_length=15,choices=MARRIED_CHOICES)
    graduatededucation=models.CharField(max_length=15,choices=GRADUATED_CHOICES)
    selfemployed=models.CharField(max_length=15,choices=SELFEMPLOYED_CHOICES)
    area=models.CharField(max_length=15,choices=PROPERTY_CHOICES)
    def __str__(self):
        return self.name
