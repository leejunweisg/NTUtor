from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

# one user mapped to one profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    verified = models.BooleanField()
    description = models.TextField()
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # override parent class's save(), to resize image on save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resize uploaded image and overwrite
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)