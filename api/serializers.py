from rest_framework import serializers

from main.models import Driver, Team, Comment

class DriverSerializer(serializers.ModelSerializer):
	class Meta:
		model = Driver
		fields = ('first_name', 'last_name', 'date_of_birth', 'country')

class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team	
		fields = ('name', 'country', 'debut_in_f1')

class DriverDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Driver
		fields = ('first_name', 'last_name', 'date_of_birth', 'country', 'image', 'team',
					'biography', 'starts', 'wins', 'pole_position', 'scores', 'best_laps')

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('driver', 'author', 'content', 'created_at')
