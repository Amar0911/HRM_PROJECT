from django.db import models

# Create your models here.

class Department(models.Model):
    dept_name=models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=300, blank=True, null=True, default=None)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.BooleanField(default=True)

    def _str_(self):
        return (self.dept_name)