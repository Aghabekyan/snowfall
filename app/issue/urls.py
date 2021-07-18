from django.urls import path
from issue.views import BugViewSet, CommentViewSet

urlpatterns = [
    path("issues", BugViewSet.as_view({"get": "list", "post": "create"}), name="bugs"),
    path(
        "issues/<int:bug_id>",
        BugViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
        ),
        name="bug-details",
    ),
    path("comments", CommentViewSet.as_view({"post": "create"}), name="comments"),
    path(
        "comments/<int:comment_id>",
        CommentViewSet.as_view({"delete": "destroy"}),
        name="comment-details",
    ),
]
