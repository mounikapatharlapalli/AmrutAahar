from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=200)  # Store hashed passwords

    def isexist(self):
        """ Check if a customer with the given email exists """
        return Customer.objects.filter(email=self.email).exists()

    @staticmethod
    def getemail(email):
        """ Retrieve customer by email, returns None if not found """
        return Customer.objects.filter(email=email).first()
    
    def check_password(self, raw_password):
        """ Check hashed password """
        return check_password(raw_password, self.password)
