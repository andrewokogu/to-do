from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import FutureSerializer, TodoSerializer
from .models import Todo
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

@swagger_auto_schema(methods=['POST'], request_body=TodoSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def todo(request):
    if request.method == 'GET':
        objs = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(objs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer =  TodoSerializer(data=request.data)
        if serializer.is_valid():
            
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')
                
            object = Todo.objects.create(**serializer.validated_data, user=request.user)
            serializer = TodoSerializer(object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=TodoSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, todo_id):
   
    try:
        obj = Todo.objects.get(id = todo_id)
    
    except Todo.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if obj.user != request.user:
        raise PermissionDenied(detail='You do not have permission to perform this action')
    
    
    if request.method == 'GET':
        serializer = TodoSerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the profile of the TODO
    elif request.method == 'PUT':
        serializer = TodoSerializer(obj, data = request.data, partial=True) 

        if serializer.is_valid():
        
            serializer.save()

            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #delete the account
    elif request.method == 'DELETE':
        obj.delete()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)
    
    
    
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def mark_complete(request, todo_id):
   
    try:
        obj = Todo.objects.get(id = todo_id)
    
    except Todo.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if obj.user != request.user:
        raise PermissionDenied(detail='You do not have permission to perform this action')
    
    
    if request.method == 'GET':
        if obj.completed == False:
            obj.completed=True
            obj.save()
                  
            data = {
                    'status'  : True,
                    'message' : "Successful"
                }

            return Response(data, status=status.HTTP_200_OK)
        else:
                  
            data = {
                    'status'  : False,
                    'message' : "Already marked complete"
                }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

    
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def today_list(request):
    if request.method == 'GET':
        today_date = timezone.now().date()
        objects = Todo.objects.filter(date=today_date, user=request.user)
        
        serializer = TodoSerializer(objects, many=True)
        data = {
            'status'  : True,
            'message' : "Successful",
            'data' : serializer.data,
        }

        return Response(data, status = status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=FutureSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def future_list(request):
    if request.method == 'POST':
        serializer = FutureSerializer(data=request.data)
        if serializer.is_valid():
            objects = Todo.objects.filter(date=serializer.validated_data['date'], user=request.user)
            
            serializer = TodoSerializer(objects, many=True)
            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_200_OK)
        else:
            error = {
                'status'  : False,
                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(error, status = status.HTTP_200_OK)




# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from .serializers import TodoSerializer
# from .models import Todo
# from drf_yasg.utils import swagger_auto_schema

# @swagger_auto_schema(methods=['POST'], request_body=TodoSerializer())
# @api_view(['GET', 'POST'])
# def todos(request):
    
#     if request.method == 'GET':
#         all_todo = Todo.objects.all() #get the data
        
#         serializer = TodoSerializer(all_todo,many=True) #serialize the data
        
#         data = {
#             "message":"success",
#             "data" : serializer.data
#         } #prepare the response data
        
        
#         return Response(data, status=status.HTTP_200_OK) #send the response
    
    
#     elif request.method == 'POST':
        
#         serializer = TodoSerializer(data=request.data)  #get and deserialize the data
        
#         if serializer.is_valid(): #check if data is valid
#             serializer.save() #save the data
#             data = {
#             "message":"success",
#             "data" : serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
        
        
#         else:
#             error = {
#                 'message':'failed',
#                 "errors":serializer.errors
#             }
    
#             return Response(error, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=TodoSerializer())
# @api_view(['GET', 'PUT', 'DELETE'])
# def todos_detail(request, todo_id):
#     """
#     Takes in a student id and returns the http response depending on the http method.
    
#     Args:
#     student_id: Interger
    
#     Allowed methods:
#     GET- Get the detail of a single student
#     PUT- Aloows the student detail to be edited
#     DELETE- This logic delets the student record from the data base
#     """
    
#     try:
#         todo_user = Todo.objects.get(id=todo_id) #get the data from the model
#     except Todo.DoesNotExist:
#         error = {
#                 'message':'failed',
#                 "errors": f"Todo user with id {todo_id} does not exist"
#             }
    
#         return Response(error, status=status.HTTP_404_NOT_FOUND)
    
    
    
#     if request.method == "GET":
#         serializer = TodoSerializer(todo_user) 
#         data = {
#             "message":"success",
#             "data" : serializer.data
#         } #prepare the response data
        
        
#         return Response(data, status=status.HTTP_200_OK) #send the response
    
#     elif request.method == "PUT":
#         serializer = TodoSerializer(todo_user, data=request.data, partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             data = {
#             "message":"success",
#             "data" : serializer.data
#             }
#             return Response(data, status=status.HTTP_202_ACCEPTED)
        
        
#         else:
#             error = {
#                 'message':'failed',
#                 "errors":serializer.errors
#             }
    
#             return Response(error, status=status.HTTP_400_BAD_REQUEST) 
        
#     elif request.method == 'DELETE':
#         todo_user.delete()
        
#         return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
    
    
 ################################################not needed######   
# @swagger_auto_schema(methods=['POST'], request_body=BookSerializer())  
# @api_view(['GET', 'POST'])
# def books(request):
    
#     if request.method == 'GET':
#         all_books = Book.objects.order_by('-created_at') #get the data
        
#         serializer = BookSerializer(all_books,many=True) #serialize the data
        
#         data = {
#             "message":"success",
#             "data" : serializer.data
#         } #prepare the response data
        
        
#         return Response(data, status=status.HTTP_200_OK) #send the response
    
    
#     elif request.method == 'POST':
        
#         serializer = BookSerializer(data=request.data)  #get and deserialize the data
        
#         if serializer.is_valid(): #check if data is valid
#             serializer.save() #save the data
#             data = {
#             "message":"success",
#             "data" : serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
        
        
#         else:
#             error = {
#                 'message':'failed',
#                 "errors":serializer.errors
#             }
    
#             return Response(error, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=BookSerializer())
# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail(request, book_id):
#     """
#     Takes in a book id and returns the http response depending on the http method.
    
#     Args:
#     book_id: Interger
    
#     Allowed methods:
#     GET- Get the detail of a single book
#     PUT- Aloows the book detail to be edited
#     DELETE- This logic delets the book record from the data base
#     """
    
#     try:
#         book = Book.objects.get(id=book_id) #get the data from the model
#     except Book.DoesNotExist:
#         error = {
#                 'message':'failed',
#                 "errors": f"Book with id {book_id} does not exist"
#             }
    
#         return Response(error, status=status.HTTP_404_NOT_FOUND)
    
    
    
#     if request.method == "GET":
#         serializer = BookSerializer(book) 
#         data = {
#             "message":"success",
#             "data" : serializer.data
#         } #prepare the response data
        
        
#         return Response(data, status=status.HTTP_200_OK) #send the response
    
#     elif request.method == "PUT":
#         serializer = BookSerializer(book, data=request.data, partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             data = {
#             "message":"success",
#             "data" : serializer.data
#             }
#             return Response(data, status=status.HTTP_202_ACCEPTED)
        
        
#         else:
#             error = {
#                 'message':'failed',
#                 "errors":serializer.errors
#             }
    
#             return Response(error, status=status.HTTP_400_BAD_REQUEST) 
        
#     elif request.method == 'DELETE':
#         book.delete()
        
#         return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
    
    
# @api_view(['GET'])
# def cohort_list(request):
#     if request.method=='GET':
#         cohorts = Student.objects.values_list('cohort', flat=True).distinct()
        
#         data = {cohort:{
#             "count":Student.objects.filter(cohort=cohort).count(),
#             "data":Student.objects.filter(cohort=cohort).values()
#             } 
                
#                 for cohort in cohorts}
        
#         return Response(data, status=status.HTTP_200_OK)