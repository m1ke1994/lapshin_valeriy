from rest_framework import serializers

from .models import CertificateItem, ContactRequest, ContentBlock, ProjectItem


class MediaUrlMixin:
    @staticmethod
    def build_media_url(request, file_field):
        if not file_field:
            return None
        url = file_field.url
        if request:
            return request.build_absolute_uri(url)
        return url


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ["id", "key", "locale", "title", "body", "extra", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectItemSerializer(MediaUrlMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectItem
        fields = [
            "id",
            "locale",
            "title",
            "description",
            "category",
            "stage",
            "meta",
            "tags",
            "image",
            "image_url",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return self.build_media_url(request, obj.image)


class CertificateItemSerializer(MediaUrlMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CertificateItem
        fields = [
            "id",
            "locale",
            "title",
            "subtitle",
            "type",
            "image",
            "image_url",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return self.build_media_url(request, obj.image)


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = [
            "id",
            "name",
            "phone",
            "preferred_date",
            "preferred_time",
            "message",
            "locale",
            "extra",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_phone(self, value):
        return value.strip()

    def create(self, validated_data):
        request = self.context.get("request")
        extra = validated_data.get("extra") or {}
        if request:
            extra.setdefault("user_agent", request.META.get("HTTP_USER_AGENT"))
            extra.setdefault("referer", request.META.get("HTTP_REFERER"))
            extra.setdefault("client_ip", request.META.get("REMOTE_ADDR"))
            extra.setdefault("path", request.path)
        validated_data["extra"] = extra
        return super().create(validated_data)
