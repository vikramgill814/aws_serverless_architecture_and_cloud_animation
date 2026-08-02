import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Find instances tagged Action=Auto-Stop
    stop_response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    stop_ids = [
        instance['InstanceId']
        for reservation in stop_response['Reservations']
        for instance in reservation['Instances']
    ]

    # Find instances tagged Action=Auto-Start
    start_response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )
    start_ids = [
        instance['InstanceId']
        for reservation in start_response['Reservations']
        for instance in reservation['Instances']
    ]

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped instances: {stop_ids}")
    else:
        print("No running Auto-Stop instances found.")

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started instances: {start_ids}")
    else:
        print("No stopped Auto-Start instances found.")

    return {
        'stopped': stop_ids,
        'started': start_ids
    }