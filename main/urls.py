from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("students", views.StudentViewSet)

urlpatterns = [
    path("", views.home, name="home"),
    path("api/health/", views.api_health, name="api-health"),
    path("api/", include(router.urls)),
    path("api/token/", views.ApiTokenView.as_view(), name="api-token"),
    path("api/schema/", views.api_schema, name="schema"),
    path("api/docs/", views.api_docs, name="swagger-ui"),
]