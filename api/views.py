from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Driver, Team
from .serializers import DriverSerializer,TeamSerializer

@api_view(['GET'])
def driver_list(request):
	if request.method == 'GET':
		drivers = Driver.objects.all()
		serializer = DriverSerializer(drivers, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def team_list(request):
	if request.method == 'GET':
		teams = Team.objects.all()
		serializer = TeamSerializer(teams, many=True)
		return Response(serializer.data)