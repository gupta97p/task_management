import string
from rest_framework import serializers
from .models import userReg

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=True)

    class Meta:
        model = userReg
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def validate_age(self, data):
        if data < 18 or data > 80:
            raise serializers.ValidationError("age must be between 17 to 80")
        return data

    def validate_gender(self, data):
        gender = ["Male", "Female", "Others"]
        if data not in gender:
            raise serializers.ValidationError("please select gender")
        return data


    def validate(self, attrs):
        if "username" in attrs:
            if " " in attrs['username']:
                raise serializers.ValidationError("username must not contain special characters except '.','_'")
            for i in string.punctuation:
                if (i != ".") and (i != "_"):
                    if i in attrs['username']:
                        raise serializers.ValidationError("username must not contain special characters except '.','_'")
        return attrs

    
    def create(self, validated_data):
        account = super().create(validated_data)
        password = validated_data['password']
        account.set_password(password)
        account.save()
        return account
