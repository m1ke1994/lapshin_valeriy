from rest_framework import mixins, viewsets
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Certificate, ContactRequest, Project, Section, SiteSettings
from .serializers import CertificateSerializer, ContactRequestSerializer, ProjectSerializer, SectionSerializer, SiteContentSerializer


class ContactRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    parser_classes = [JSONParser, FormParser]
    permission_classes = [AllowAny]
    authentication_classes = []
    http_method_names = ["post", "head", "options"]


class SiteContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.objects.first()
        sections = Section.objects.filter(is_enabled=True).prefetch_related("items").order_by("order", "id")
        projects = Project.objects.filter(is_published=True).order_by("order", "id")
        certificates = Certificate.objects.filter(is_published=True).order_by("order", "id")

        data = {
            "settings": settings,
            "sections": sections,
            "projects": projects,
            "certificates": certificates,
        }
        serializer = SiteContentSerializer(instance=data, context={"request": request})
        return Response(serializer.data)
