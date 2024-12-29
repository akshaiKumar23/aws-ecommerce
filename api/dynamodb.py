import boto3
import json
from django.conf import settings
from decimal import Decimal
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME
)
sns = boto3.client('sns', region_name=settings.AWS_REGION_NAME)
sqs = boto3.resource('sqs', region_name=settings.AWS_REGION_NAME)

PRODUCT_SNS_TOPIC = "arn:aws:sns:ap-south-1:203918841131:ProductUpdates"
INTERACTION_SQS_QUEUE = "AdminQueue"


products_table = dynamodb.Table(settings.DYNAMODB_TABLES['Products'])
interactions_table = dynamodb.Table(settings.DYNAMODB_TABLES['Interactions'])


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object is not JSON serializable")


def publish_to_sns(topic_arn, action, product_data):
    message = {
        'action': action,
        'product': product_data
    }
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message, default=decimal_default)
    )
    return response


def fetch_messages_from_sqs(queue_name):
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    messages = queue.receive_messages(MaxNumberOfMessages=10)
    for message in messages:
        process_interaction_event(json.loads(message.body))
        message.delete()


def process_interaction_event(event):
    interactions_table.put_item(Item=event)
