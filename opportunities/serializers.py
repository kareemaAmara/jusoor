from rest_framework import serializers
from .models import Category, Opportunity
from users.models import Organization


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class OrganizationMiniSerializer(serializers.ModelSerializer):
    """Lightweight organization info to embed inside Opportunity."""
    class Meta:
        model = Organization
        fields = ['id', 'org_name', 'verified']


class OpportunityListSerializer(serializers.ModelSerializer):
    """Used when listing opportunities (lighter version)."""
    organization = OrganizationMiniSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'description', 'category', 'location',
            'start_date', 'end_date', 'hours', 'capacity', 'deadline',
            'status', 'image', 'organization', 'applications_count', 'created_at'
        ]

    def get_applications_count(self, obj):
        return obj.applications.count()


class OpportunityDetailSerializer(OpportunityListSerializer):
    """Used for detail view (same as list for now, can be extended)."""
    pass


class OpportunityCreateUpdateSerializer(serializers.ModelSerializer):
    """Used for creating & updating opportunities."""
    category_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'description', 'category_id', 'location',
            'start_date', 'end_date', 'hours', 'capacity', 'deadline',
            'status', 'image'
        ]

    def create(self, validated_data):
        # organization is set in the view from the logged-in user
        category_id = validated_data.pop('category_id', None)
        request = self.context.get('request')
        organization = Organization.objects.get(user=request.user)
        opportunity = Opportunity.objects.create(
            organization=organization,
            category_id=category_id,
            **validated_data
        )
        return opportunity

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        if category_id is not None:
            instance.category_id = category_id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance