from django.db import models


class Doctor(models.Model):

    name = models.CharField(max_length=100)

    specialization = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.name


class Patient(models.Model):

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Approved', 'Approved'),

        ('Completed', 'Completed'),

    )
    
    token = models.IntegerField(default=1)

    name = models.CharField(max_length=100)

    age = models.IntegerField()

    gender = models.CharField(max_length=10)

    phone = models.CharField(max_length=15)

    date = models.DateField()

    time = models.TimeField()

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):

        return self.name