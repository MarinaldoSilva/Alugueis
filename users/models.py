from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    """
        AbstractUser: Já tem em si username, email, first/last_name e password
    """