from rest_framework import serializers

from applications.shop_wallet.models import ShopWallet


class ShopWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopWallet
        fields = '__all__'

    def create(self, validated_data):
        validated_data['current_balance'] = 20
        return ShopWallet.objects.create(**validated_data)