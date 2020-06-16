from rest_framework import viewsets
from rest_framework.response import Response

from applications.user_wallet.models import UserWallet
from applications.user_wallet.serializers import UserWalletSerializer


class UserWalletViewSet(viewsets.ModelViewSet):
    serializer_class = UserWalletSerializer
    queryset = UserWallet.objects.all()

    def get_queryset(self):
        req = self.request
        wallet_address = req.query_params.get('wallet_address')
        queryset = UserWallet.objects.filter(wallet_address=wallet_address)
        return queryset