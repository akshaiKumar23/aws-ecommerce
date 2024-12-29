from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .dynamodb import products_table, publish_to_sns, fetch_messages_from_sqs, interactions_table, INTERACTION_SQS_QUEUE, PRODUCT_SNS_TOPIC
from boto3.dynamodb.conditions import Attr


class ProductListCreateView(APIView):
    def get(self, request):
        products = products_table.scan().get('Items', [])
        return Response(products, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_data = serializer.validated_data
            products_table.put_item(Item=product_data)
            publish_to_sns(
                topic_arn=PRODUCT_SNS_TOPIC,
                action='add',
                product_data=product_data
            )
            return Response(product_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InteractionView(APIView):
    def get(self, request, product_id):
        fetch_messages_from_sqs(INTERACTION_SQS_QUEUE)

        response = interactions_table.scan(
            FilterExpression=Attr('product_id').eq(product_id)
        )
        interactions = response.get('Items', [])
        return Response(interactions, status=status.HTTP_200_OK)
