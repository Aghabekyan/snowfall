from django.contrib.auth import get_user_model
from django.db import models
from helpers.choices import StatusType

User = get_user_model()


class Bug(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=False)
    body = models.CharField(max_length=255, null=True, blank=False)
    status = models.IntegerField(
        choices=StatusType.choices, default=StatusType.UNRESOLVED
    )
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bugs", null=True
    )

    class Meta:
        ordering = ["id"]
        db_table = "bug"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=False)
    body = models.CharField(max_length=255, null=True, blank=False)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="comments")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        db_table = "comment"
