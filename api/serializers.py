from rest_framework import serializers
from .choices import TEAM_CHOICES


class SelectTeamSerializer(serializers.Serializer):
    home_team = serializers.ChoiceField(choices=TEAM_CHOICES)
    away_team = serializers.ChoiceField(choices=TEAM_CHOICES)