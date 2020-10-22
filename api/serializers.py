from rest_framework import serializers

from main.models import Driver, Team

class DriverSerializer(serializers.ModelSerializer):
	class Meta:
		model = Driver
		fields = ('first_name', 'last_name', 'date_of_birth', 'country')

class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team	
		fields = ('name', 'country', 'debut_in_f1')

