from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.timezone import localtime
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import pytz

from applications.coupons.models import Coupon
from applications.coupons.serializers import CouponSerializer, CouponRedeemSerializer
from applications.shops.models import Shop


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()

    def send_mail_to_shop(self, coupon, shop):
        def get_local_time(time):
            tz = pytz.timezone('Asia/Taipei')
            return localtime(time, tz).strftime('%Y-%m-%d %H:%M:%S')

        message = ('兌換資訊\n' +
            '商家名稱：{}\n'.format(shop.name) +
            '兌換券序號：{}\n'.format(coupon.id) +
            '兌換時間：{}\n'.format(get_local_time(coupon.redeemed_time)))
        send_mail(
            'MyLog 折價券兌換通知'.format(coupon.id),
            message,
            'hi@numbersprotocol.io',
            [shop.email],
            fail_silently=False,
        )

    @action(detail=True, methods=['post'])
    def redeem(self, request, pk=None):
        coupon = self.get_object()
        serializer = CouponRedeemSerializer(data=request.data, context={'coupon': coupon})
        if serializer.is_valid():
            serializer.save()
            self.send_mail_to_shop(coupon, serializer.instance.redeemed_shop)
            coupon_serializer = CouponSerializer(serializer.instance)
            return Response(coupon_serializer.data, status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)