import boto3
import json

sns = boto3.client('sns')

# Replace with your actual SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-west-1:975050024946:ec2-state-change-alert'


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # EventBridge sends EC2 state-change events with this structure:
    # event['detail']['instance-id'] and event['detail']['state']
    detail = event.get('detail', {})
    instance_id = detail.get('instance-id', 'UNKNOWN')
    state = detail.get('state', 'UNKNOWN')
    region = event.get('region', 'UNKNOWN')
    time = event.get('time', 'UNKNOWN')

    message = (
        f"EC2 Instance State Change Detected\n\n"
        f"Instance ID: {instance_id}\n"
        f"New State: {state}\n"
        f"Region: {region}\n"
        f"Time: {time}"
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"EC2 Alert: Instance {instance_id} is now {state}",
        Message=message
    )

    print(f"Notification sent for instance {instance_id} -> {state}")

    return {
        'instance_id': instance_id,
        'state': state
    }
