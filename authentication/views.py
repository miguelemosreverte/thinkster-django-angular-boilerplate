import json
from rest_framework import viewsets, permissions, status, views
from models import Account
from serializers import AccountSerializer
from rest_framework.response import Response
from permissions import IsAccountOwner
from django.contrib.auth import authenticate, login

# Create your views here.


class AccountViewSet(viewsets.ModelViewSet):
	lookup_field = 'username'
	#http://localhost:8000/api/v1/accounts/<username>

	queryset = Account.objects.all()
	serializer_class = AccountSerializer

	#restrict access

	def get_permission(self):

		print 'checking'

		if self.request.method in permissions.SAFE_METHODS:
			return (permissions.AllowAny(),)

		if self.request.method == 'POST':
			print "POSTED from authentication.models import Account"
			return (permissions.AllowAny(),)


		return(permissions.IsAuthenticated(), IsAccountOwner(),)

	def create(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			Account.objects.create_user(**serializer.validated_data)

			return Response(
				serializer.validated_data, 
				status=status.HTTP_201_CREATED
				)

		#if serializer is not valiud
		print serializer.errors

		return Response({
			'status':'Bad request',
			'message':'Account could not be created with recieved data.'
			}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
	def post(self, request, format=None):
		data = json.loads(request.body)
		email =  data.get('email', None)
		password = data.get('password', None)

		account =  authenticate(email=email, password=password)

		if account is not None:
			if account.is_active:
				login(request, account)
				serialized = AccountSerializer(account)
				return Response(serialized.data)
			else:
				return Response({
					'status' : 'Unauthorized',
					'message' : 'Account has been disabled',

					}, status=status.HTTP_401_UNAUTHORIZED)

		else:
			return Response({
				'status': 'Unauthorized',
				'message':'Email/Password combination is invalid'
				}, status=status.HTTP_401_UNAUTHORIZED)








