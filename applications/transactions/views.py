from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.timezone import localtime
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import pytz

from applications.transactions.models import Transaction
from applications.transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def send_mail_to_shop(self, transaction):
        def get_local_time(time):
            tz = pytz.timezone('Asia/Taipei')
            return localtime(time, tz).strftime('%Y-%m-%d %H:%M:%S')

        message = ('交易資訊\n' +
            '交易款項：{}元\n'.format(transaction.points) +
            '支付者錢包：{}\n'.format(transaction.sender.wallet_address) +
            '收取者錢包：{}\n'.format(transaction.recipient.wallet_address) +
            '交易編號{}\n'.format(transaction.id) +
            '交易時間：{}\n'.format(get_local_time(transaction.transaction_time)))
        send_mail(
            'MyLog 錢包交易通知',
            message,
            'hi@numbersprotocol.io',
            [transaction.recipient.email],
            fail_silently=False,
        )

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.send_mail_to_shop(serializer.instance)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)