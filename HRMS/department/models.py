from django.db import models

# Create your models here.

class Department(models.Model):
    Dept_Name=models.CharField(max_length=100)
    Description = models.CharField(max_length=300, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.BooleanField(default=True)

    def _str_(self):
        return (self.Dept_Name)