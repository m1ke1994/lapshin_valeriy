from typing import Dict

from rest_framework import mixins, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CertificateItem, ContactRequest, ContentBlock, ProjectItem
from .serializers import CertificateItemSerializer, ContactRequestSerializer, ContentBlockSerializer, ProjectItemSerializer
from .services import collect_sections


class ContentBlockViewSet(viewsets.ModelViewSet):
    serializer_class = ContentBlockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = ContentBlock.objects.all()
        locale = self.request.query_params.get("locale")
        if locale:
            qs = qs.filter(locale=locale)
        return qs.order_by("key", "locale")


class ProjectItemViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectItemSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = ProjectItem.objects.all()
        locale = self.request.query_params.get("locale")
        if locale:
            qs = qs.filter(locale=locale)
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_active=True)
        return qs.order_by("order", "id")


class CertificateItemViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateItemSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = CertificateItem.objects.all()
        locale = self.request.query_params.get("locale")
        if locale:
            qs = qs.filter(locale=locale)
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_active=True)
        return qs.order_by("order", "id")


class ContactRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    parser_classes = [JSONParser, FormParser]
    permission_classes = [AllowAny]
    authentication_classes = []
    http_method_names = ["post", "head", "options"]


class HomePublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale") or "ru"
        blocks: Dict[str, ContentBlock] = {
            block.key: block for block in ContentBlock.objects.filter(locale=locale)
        }
        data = collect_sections(blocks)

        projects_qs = ProjectItem.objects.filter(locale=locale, is_active=True).order_by("order", "id")
        certs_qs = CertificateItem.objects.filter(locale=locale, is_active=True).order_by("order", "id")

        data["projects"]["items"] = ProjectItemSerializer(
            projects_qs, many=True, context={"request": request}
        ).data
        data["certificates"]["items"] = CertificateItemSerializer(
            certs_qs, many=True, context={"request": request}
        ).data

        return Response({"locale": locale, "home": data})
