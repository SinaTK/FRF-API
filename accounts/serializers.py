from rest_framework import serializers
from django.contrib.auth.models import User


def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin can not be in email')

class RegisterSerializer(serializers.ModelSerializer):
    
    ## Using Serializers
    # username = serializers.CharField(required=True)
    # email = serializers.EmailField(required=True, validators=[clean_email])
    # password = serializers.CharField(required=True, write_only=True)
       
    password_2 = serializers.CharField(required=True, write_only=True)

    ## Using ModelSerializers
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_2']
        extra_kwargs = {
            'email': {'validators':[clean_email]},
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        del validated_data['password_2']
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError("Username can't be admin")            
        return value
    
    def validate(self, data):
        if data['password'] != data['password_2']:
            raise serializers.ValidationError("Passwords aren't match")     
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'