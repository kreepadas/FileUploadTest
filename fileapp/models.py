from django.db import models

class Employee(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone_Number = models.PositiveIntegerField(blank=True)
    age = models.PositiveIntegerField(blank=True)


    def __str__(self):
        return '{} {}'.format(self.Name, self.Email)



