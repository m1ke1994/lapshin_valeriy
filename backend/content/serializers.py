from rest_framework import serializers

from .models import Certificate, ContactRequest, Project, Section, SectionItem, SiteSettings


class SectionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionItem
        fields = [
            "id",
            "item_type",
            "title_ru",
            "title_en",
            "text_ru",
            "text_en",
            "value_ru",
            "value_en",
            "order",
            "is_enabled",
        ]
        read_only_fields = ["id"]


class SectionSerializer(serializers.ModelSerializer):
    items = SectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = [
            "id",
            "type",
            "title_ru",
            "title_en",
            "subtitle_ru",
            "subtitle_en",
            "body_ru",
            "body_en",
            "button_text_ru",
            "button_text_en",
            "button_link",
            "is_enabled",
            "order",
            "items",
        ]
        read_only_fields = ["id"]


class ProjectSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title_ru",
            "title_en",
            "description_ru",
            "description_en",
            "category_ru",
            "category_en",
            "stage_ru",
            "stage_en",
            "tags_ru",
            "tags_en",
            "link",
            "image",
            "image_url",
            "order",
            "is_published",
        ]
        read_only_fields = ["id", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class CertificateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "title_ru",
            "title_en",
            "issuer_ru",
            "issuer_en",
            "year",
            "description_ru",
            "description_en",
            "image",
            "image_url",
            "file",
            "file_url",
            "order",
            "is_published",
        ]
        read_only_fields = ["id", "image_url", "file_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "site_name_ru",
            "site_name_en",
            "header_cta_text_ru",
            "header_cta_text_en",
            "header_cta_link",
            "email",
            "phone",
            "address",
        ]


class SiteContentSerializer(serializers.Serializer):
    settings = SiteSettingsSerializer(allow_null=True)
    sections = SectionSerializer(many=True)
    projects = ProjectSerializer(many=True)
    certificates = CertificateSerializer(many=True)


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
