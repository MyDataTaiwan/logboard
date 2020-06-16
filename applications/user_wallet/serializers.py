from rest_framework import serializers

from applications.user_wallet.models import UserWallet


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = '__all__'

    def create(self, validated_data):
        validated_data['current_balance'] = 20
        return UserWallet.objects.create(**validated_data)