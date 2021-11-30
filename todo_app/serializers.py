from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = '__all__'
        
class FutureSerializer(serializers.Serializer):
    date = serializers.DateField()

# from rest_framework import serializers
# from .models import Todo


# class TodoSerializer(serializers.ModelSerializer):
   
    
#     class Meta:
#         model = Todo
#         fields = ['id', 'name', 'title', 'body', 'created_at']
        
        
        
