from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()


class InteractionSerializer(serializers.Serializer):
    interaction_id = serializers.CharField(max_length=255, required=False)
    product_id = serializers.CharField(max_length=255)
    user_id = serializers.CharField(max_length=255)
    interaction_type = serializers.ChoiceField(
        choices=['like', 'comment', 'order'])
    content = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(read_only=True)
