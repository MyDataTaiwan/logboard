from rest_framework import serializers

from applications.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        sender = validated_data['sender']
        recipient = validated_data['recipient']
        points = validated_data['points']
        sender.current_balance -= points
        recipient.current_balance += points
        recipient.accumulated_redeem_balance += points
        sender.save()
        recipient.save()
        return Transaction.objects.create(**validated_data)

    def validate(self, data):
        if data['sender'].current_balance < data['points']:
            raise serializers.ValidationError('Current balance is insufficient')

        return data