from django.contrib.auth import get_user_model
from issue.models import Bug, Comment
from rest_framework import serializers

User = get_user_model()


class BugSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, source="user", allow_null=True
    )

    class Meta:
        model = Bug
        fields = ["id", "title", "body", "status", "user_id"]
        extra_kwargs = {"title": {"required": True}, "body": {"required": True}}


class CommentSerializer(serializers.ModelSerializer):
    bug_id = serializers.PrimaryKeyRelatedField(
        queryset=Bug.objects.all(), required=True, source="bug"
    )

    class Meta:
        model = Comment
        fields = ["id", "title", "body", "bug_id"]
        extra_kwargs = {"title": {"required": True}, "body": {"required": True}}
