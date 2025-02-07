from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from users.serializers import LoginSerializer, SignUpSerializer, UserResponseSerializer
from utils.jwt import create_jwt_pair_for_user

# Create your views here.


class SignUpView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully"}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request: Request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:

            payload = create_jwt_pair_for_user(user)

            response = {
                "message": "Login Successfull",
                "payload": payload
                }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Please provide a valid phone number and password"})


@api_view(['GET'])
def me(request):
    user = request.user
    serializer = UserResponseSerializer(user)

    return Response(data=serializer.data)