from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=15)

    class Meta:
        db_table = "user"


class Role(models.Model):
    role_name = models.CharField(max_length=50)

    class Meta:
        db_table = "role"


class UserRole(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "userrole"



