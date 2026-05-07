from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()

    avail_roles = [
        ("Regular", "Regular"),
        ("Book Contributor", "Book Contributor"),
        ("Commission Maker", "Commission Maker"),
        ("Project Creator", "Project Creator"),
        ("Event Organizer", "Event Organizer"),
        ("Market Seller", "Market Seller"),
    ]
    role = models.CharField(max_length=50, choices=avail_roles, default="Regular")

    def __str__(self):
        return self.display_name 