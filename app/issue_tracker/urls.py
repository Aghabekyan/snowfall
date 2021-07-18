from django.conf.urls import url
from django.urls import include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    url("api/schema/$", SpectacularAPIView.as_view(), name="schema"),
    url(
        "swagger-docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns = urlpatterns + [
    url(r"api/v1/", include(("issue.urls", "issues"), namespace="issues")),
]
