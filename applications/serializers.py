from rest_framework import serializers
from .models import Application, Participation
from users.models import User
from opportunities.models import Opportunity


class VolunteerMiniSerializer(serializers.ModelSerializer):
    """Lightweight volunteer info to embed inside Application."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'profile_image', 'skills']


class OpportunityMiniSerializer(serializers.ModelSerializer):
    """Lightweight opportunity info to embed inside Application."""
    class Meta:
        model = Opportunity
        fields = ['id', 'title', 'location', 'start_date', 'hours']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Used when a volunteer applies to an opportunity."""
    class Meta:
        model = Application
        fields = ['id', 'opportunity']

    def validate(self, data):
        request = self.context.get('request')
        volunteer = request.user
        opportunity = data['opportunity']

        # Check 1: User must be a volunteer
        if volunteer.role != 'volunteer':
            raise serializers.ValidationError({'error': 'Only volunteers can apply'})

        # Check 2: Opportunity must be open
        if opportunity.status != 'open':
            raise serializers.ValidationError({'error': 'Opportunity is not open for applications'})

        # Check 3: User hasn't already applied
        if Application.objects.filter(volunteer=volunteer, opportunity=opportunity).exists():
            raise serializers.ValidationError({'error': 'You have already applied to this opportunity'})

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['volunteer'] = request.user
        return Application.objects.create(**validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):
    """Used for listing applications (volunteer or organization view)."""
    volunteer = VolunteerMiniSerializer(read_only=True)
    opportunity = OpportunityMiniSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'volunteer', 'opportunity', 'status', 'applied_date', 'feedback']


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """Used by organizations to accept/reject applications."""
    class Meta:
        model = Application
        fields = ['id', 'status', 'feedback']

    def validate_status(self, value):
        allowed_statuses = ['accepted', 'rejected', 'under_review']
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Status must be one of {allowed_statuses}")
        return value


class ParticipationSerializer(serializers.ModelSerializer):
    """Participation records (verified volunteer hours)."""
    volunteer = VolunteerMiniSerializer(read_only=True)
    opportunity = OpportunityMiniSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ['id', 'volunteer', 'opportunity', 'hours_completed', 'verified', 'completion_date']


class ParticipationCreateSerializer(serializers.ModelSerializer):
    """Used by organization to record volunteer hours."""
    class Meta:
        model = Participation
        fields = ['id', 'volunteer', 'opportunity', 'hours_completed', 'completion_date']

    def create(self, validated_data):
        request = self.context.get('request')
        from users.models import Organization
        try:
            org = Organization.objects.get(user=request.user)
            validated_data['verified_by'] = org
            validated_data['verified'] = True
        except Organization.DoesNotExist:
            pass
        return Participation.objects.create(**validated_data)