from rest_framework import serializers

from .models import *

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    user_id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['user'] = UserSerializer(
                User.objects.get(pk=data['user'])).data
        return data

class loanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = loanPayment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['user'] = UserSerializer(
                User.objects.get(pk=data['user'])).data
        return data


class requestLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = requestLoan
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['user'] = UserSerializer(
                User.objects.get(pk=data['user'])).data
        return data