from rest_framework import serializers
from .models import  RegisteredUsers

#Serializer for RegisteredUsers Model
class RegisteredUsersSerializer(serializers.ModelSerializer) :
    class Meta :
        model = RegisteredUsers
        fields = ['id','name','email','password']

        #Making sure password is write-only(for security purpose)
        extra_kwargs ={
            'password' : {'write_only' : True}
        }


    def create(self, validated_data):
        pwd = validated_data.pop('password')
        
        #Retrieving the password from the latest registered entry
        current_entry = self.Meta.model(**validated_data)

        #Stoing the password in hash form in th database
        current_entry.set_password(pwd)

        current_entry.save()

        return current_entry