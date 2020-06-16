from rest_framework import viewsets
from rest_framework.response import Response

from applications.shop_wallet.models import ShopWallet
from applications.shop_wallet.serializers import ShopWalletSerializer


class ShopWalletViewSet(viewsets.ModelViewSet):
    serializer_class = ShopWalletSerializer
    queryset = ShopWallet.objects.all()

    def get_queryset(self):
        req = self.request
        wallet_address = req.query_params.get('wallet_address')
        queryset = ShopWallet.objects.filter(wallet_address=wallet_address)
        return queryset