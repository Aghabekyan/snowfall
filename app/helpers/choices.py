from django.db import models


class StatusType(models.IntegerChoices):
    RESOLVED = 1
    UNRESOLVED = 2
