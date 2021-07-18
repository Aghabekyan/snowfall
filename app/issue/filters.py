from django_filters import rest_framework as filters
from issue.models import Bug


class BugFilter(filters.FilterSet):
    class Meta:
        model = Bug
        fields = ["status"]
