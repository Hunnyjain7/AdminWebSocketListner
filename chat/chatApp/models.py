import os
import sys
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from io import BytesIO
from PIL import Image


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    password = models.CharField(max_length=15)

    def save(self):
        # Opening the uploaded image

        im = Image.open(self.profile_image)
        output = BytesIO()
        # Resize/modify the image

        check_size = self.profile_image.size / 1024
        if check_size > 1024:
            print("more than 1 mb")
            im = im.resize((1024, 1024))
        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=60)
        output.seek(0)
        # change the imagefield value to be the newley modifed image value
        self.profile_image = InMemoryUploadedFile(output, 'ImageField',
                                                  "%s.jpg" % str(uuid.uuid4()),
                                                  'profile_image/jpeg',
                                                  sys.getsizeof(output), None)
        super(User, self).save()

    @property
    def role(self):
        return UserRole.objects.get(user_id=self.id)

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
        db_table = "user_role"

    @staticmethod
    def admins():
        roles = UserRole.objects.filter(role_id=1)
        users = []
        for user in roles:
            users.append(user.user_id)
        return users
