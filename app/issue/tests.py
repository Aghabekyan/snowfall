from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from helpers.choices import StatusType
from issue.models import Bug, Comment
from issue.serializers import BugSerializer
from model_bakery import baker
from rest_framework import status

User = get_user_model()


class BugTestCase(TestCase):
    APPLICATION_JSON = "application/json"

    def setUp(self):
        self.user = User.objects.create(username="username", first_name="John")
        self.user.set_password("Qwer1234!")
        self.user.save()

        self.client = Client()

        self.endpoints = {
            "issues-bugs": (lambda x=None: reverse("issues:bugs", args=x)),
            "issues-bug-details": (
                lambda x=None: reverse("issues:bug-details", args=x)
            ),
            "issues-comments": (lambda x=None: reverse("issues:comments", args=x)),
            "issues-comment-details": (
                lambda x=None: reverse("issues:comment-details", args=x)
            ),
        }

    def test_get_bugs_ok(self):
        bug = baker.make(Bug)
        endpoint = self.endpoints.get("issues-bugs")()
        resp = self.client.get(endpoint, content_type=self.APPLICATION_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["count"], 1)
        data = BugSerializer(bug).data
        self.assertDictEqual(resp.json()["results"][0], data)

    def test_get_unresolved_bugs_ok(self):
        unresolved_bug = baker.make(Bug, status=StatusType.UNRESOLVED)
        baker.make(Bug, status=StatusType.RESOLVED)
        endpoint = self.endpoints.get("issues-bugs")()
        resp = self.client.get(
            f"{endpoint}?status={StatusType.UNRESOLVED}",
            content_type=self.APPLICATION_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["count"], 1)
        data = BugSerializer(unresolved_bug).data
        self.assertDictEqual(resp.json()["results"][0], data)

    def test_create_bug_ok(self):
        endpoint = self.endpoints.get("issues-bugs")()
        data = {"title": "title", "body": "body"}
        resp = self.client.post(endpoint, data=data, content_type=self.APPLICATION_JSON)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_bug_details_ok(self):
        bug = baker.make(Bug)
        endpoint = self.endpoints.get("issues-bug-details")([bug.id])
        resp = self.client.get(endpoint, content_type=self.APPLICATION_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = BugSerializer(bug).data
        self.assertDictEqual(resp.json(), data)

    def test_change_bug_status_ok(self):
        bug = baker.make(Bug, status=StatusType.UNRESOLVED)
        endpoint = self.endpoints.get("issues-bug-details")([bug.id])
        data = {"status": StatusType.RESOLVED}
        resp = self.client.patch(
            endpoint, data=data, content_type=self.APPLICATION_JSON
        )
        bug.refresh_from_db()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(bug.status, StatusType.RESOLVED)

    def test_delete_bug_ok(self):
        bug = baker.make(Bug, is_deleted=False)
        endpoint = self.endpoints.get("issues-bug-details")([bug.id])
        resp = self.client.delete(endpoint, content_type=self.APPLICATION_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        bug.refresh_from_db()
        self.assertEqual(bug.is_deleted, True)

    def test_create_bug_comment_ok(self):
        bug = baker.make(Bug, is_deleted=False)
        endpoint = self.endpoints.get("issues-comments")()
        data = {"title": "title", "body": "body", "bug_id": bug.id}
        resp = self.client.post(endpoint, data=data, content_type=self.APPLICATION_JSON)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_delete_bug_comment_ok(self):
        bug = baker.make(Bug, is_deleted=False)
        comment = baker.make(Comment, bug=bug, is_deleted=False)
        endpoint = self.endpoints.get("issues-comment-details")([comment.id])
        resp = self.client.delete(endpoint, content_type=self.APPLICATION_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        comment.refresh_from_db()
        self.assertEqual(comment.is_deleted, True)
