from django_filters.rest_framework import DjangoFilterBackend
from issue.filters import BugFilter
from issue.models import Bug, Comment
from issue.serializers import BugSerializer, CommentSerializer
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination


class BugViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BugSerializer
    queryset = Bug.objects.filter(is_deleted=False)
    pagination_class = LimitOffsetPagination
    filter_class = BugFilter
    filter_backends = (DjangoFilterBackend,)
    lookup_field = "pk"
    lookup_url_kwarg = "bug_id"

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    lookup_field = "pk"
    lookup_url_kwarg = "comment_id"

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
