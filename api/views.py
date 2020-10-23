from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from main.models import Driver, Team, Comment
from .serializers import *

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

class DriverDetailView(RetrieveAPIView):
	queryset = Driver.objects.filter(is_active=True)
	serializer_class = DriverDetailSerializer	

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
	if request.method == 'POST':
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	
	else:
		comments = Comment.objects.filter(is_active=True, driver=pk)
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)		