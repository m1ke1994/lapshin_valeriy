from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CertificateItemViewSet,
    ContactRequestViewSet,
    ContentBlockViewSet,
    HomePublicView,
    ProjectItemViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectItemViewSet, basename="project")
router.register(r"certificates", CertificateItemViewSet, basename="certificate")
router.register(r"content", ContentBlockViewSet, basename="content")
router.register(r"applications", ContactRequestViewSet, basename="application")

urlpatterns = [
    path("public/home/", HomePublicView.as_view(), name="public-home"),
    path("", include(router.urls)),
]
