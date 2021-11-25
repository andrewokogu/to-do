from django.http import response
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import ChangePasswordSerializer, UserSerializer, LoginSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(methods=['POST'], request_body=LoginSerializer())
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                if user.is_active:
                    serializer = UserSerializer(user)
                    data = {
                        'message':'Login Successful',
                        'data':serializer.data
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    error = {
                        'message':'Please activate your account',
                    }    
                    return Response(error, status=status.HTTP_401_UNAUTHORIZED)
            else:
                error = {
                    "errors":serializer.errors
                }
                return Response(error, status=status.HTTP_401_UNAUTHORIZED)


User = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body=UserSerializer())
@api_view(['GET', 'POST'])
def users(request):
    
    if request.method == 'GET':
        all_users = User.objects.filter(is_active=True) #get the data
        
        serializer = UserSerializer(all_users,many=True) #serialize the data
        
        data = {
            "message":"success",
            "data" : serializer.data
        } #prepare the response data
        
        
        return Response(data, status=status.HTTP_200_OK) #send the response
    
    
    elif request.method == 'POST':
        
        serializer = UserSerializer(data=request.data)  #get and deserialize the data
        
        if serializer.is_valid(): #check if data is valid
            serializer.validated_data['password'] = make_password(serializer.validated_data['password']) #hash the password
            
            user = User.objects.create(**serializer.validated_data)
            user_serializer = UserSerializer(user)
            
            data = {
            "message":"success",
            "data" : user_serializer.data
            }
            
            return Response(data, status=status.HTTP_201_CREATED)
        
        
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


    
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=UserSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    
    try:
        user = User.objects.get(id=user_id) #get the data from the model
    except User.DoesNotExist:
        error = {
                'message':'failed',
                "errors": f"User with id {user_id} does not exist"
            }
    
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    
    
    
    if request.method == "GET":
        serializer = UserSerializer(user) 
        data = {
            "message":"success",
            "data" : serializer.data
        } #prepare the response data
        
        
        return Response(data, status=status.HTTP_200_OK) #send the response
    
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            if 'password' in serializer.validated_data.keys():
                raise ValidationError("Unable to change password")
            
            serializer.save()
            data = {
            "message":"success",
            "data" : serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        
        
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
        
    elif request.method == 'DELETE':
        user.delete()
        
        return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
    

@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    # print(user.password)
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):
                
                user.set_password(serializer.validated_data['new_password'])
                
                user.save()
                
                # print(user.password)
                
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            
            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
            
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
