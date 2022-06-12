from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404 
from rest_framework import generics, mixins, viewsets, filters


from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

# Create your views here.
def no_rest_from_model(request):
	data = Guest.objects.all()
	response = {
		'guests': list(data.values('name', 'mobile'))
	}
	return JsonResponse(response)


# GET POST
@api_view(['GET', 'POST'])
def FBV_List(request):
	# GET
	if request.method == 'GET':
		guests = Guest.objects.all()
		serializer = GuestSerializer(guests, many=True)
		return Response(serializer.data)

	# POST
	elif request.method == 'POST':
		serializer = GuestSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
	try:
		guest = Guest.objects.get(pk=pk)
	except Guest.DoesNotExists:
		return Response(status=status.HTTP_404_NOT_FOUND)

	# GET
	if request.method == 'GET':
		serializer = GuestSerializer(guest)
		return Response(serializer.data)

	# PUT
	elif request.method == 'PUT':
		serializer = GuestSerializer(guest, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# DELETE
	elif request.method == 'DELETE':
		guest.delete()
		return Response(Status=status.HTTP_204_NO_CONTENT)


# CBV
class CBV_List(APIView):
	def get(self, request):
		guests = Guest.objects.all()
		serializer = GuestSerializer(guests, many=True)
		return Response(serializer.data)
	def post(self, request):
		serializer = GuestSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				serializer.data,
				status = status.HTTP_201_CREATED
			)
		return Response(
			serializer.data,
			status = status.HTTP_400_BAD_REQUEST
		)


class CBV_pk(APIView):
	def get_object(self, pk):
		try:
			return Guest.objects.get(pk=pk)
		except Guest.DoesNotExists:
			raise Http404
	def get(self, request, pk):
		guest = self.get_object(pk)
		serializer = GuestSerializer(guest)
		return Response(
			serializer.data,
			status = status.HTTP_201_CREATED
		)

	def put(self, request, pk):
		guest = self.get_object(pk)
		serializer = GuestSerializer(guest, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(
			serializer.errors, 
			status = status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, pk):
		guest = self.get_object(pk)
		guest.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


# Mixins
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer

	def get(self, request):
		return self.list(request)
	def post(self, request):
		return self.create(request)


class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer

	def get(self, request, pk):
		return self.retrieve(request)
	def put(self, request, pk):
		return self.update(request)
	def delete(self, request, pk):
		return self.destroy(request)


#  Generics
class generics_list(generics.ListCreateAPIView):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer
	# authentication_classes = [BasicAuthentication]
	authentication_classes = [TokenAuthentication]
	# permission_classes = [IsAuthenticated]


class generics_pk(generics.RetrieveUpdateDestroyAPIView):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer
	# Login requirement:
	# authentication_classes = [BasicAuthentication]

	# Token requirement
	authentication_classes = [TokenAuthentication]
	# permission_classes = [IsAuthenticated]


# Viewsets
# Guests
class viewsets_guest(viewsets.ModelViewSet):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer


# Movie
class viewsets_movie(viewsets.ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	filter_backend = [filters.SearchFilter]
	search_fields = ['movie']


# Reservation
class viewsets_reservation(viewsets.ModelViewSet):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer


# Find a movie
@api_view(['GET'])
def find_movie(request):
	movies = Movie.objects.filter(
		hall = request.data['hall'],
		movie = request.data['movie'],
	)
	serializer = MovieSerializer(movies, many=True)
	return Response(serializer.data)


# Create a new reservaion
@api_view(['POST'])
def new_reservation(request):
	movie = Movie.objects.get(
		hall =request.data['hall'],
		movie = request.data['movie']
		)

	guest = Guest()
	guest.name = request.data['name']
	guest.mobile = request.data['mobile']
	guest.save()

	reservation = Reservation()
	reservation.guest = guest
	reservation.movie = movie 
	reservation.save()

	return Response(status=status.HTTP_201_CREATED)



# Post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthorOrReadOnly]
	queryset = Post.objects.all()
	serializer_class = PostSerializer