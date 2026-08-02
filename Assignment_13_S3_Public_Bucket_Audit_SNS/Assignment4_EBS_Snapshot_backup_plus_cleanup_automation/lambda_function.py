import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

# Replace with your actual EBS volume ID
VOLUME_ID = 'vol-06deac550b279d166'

# Snapshots older than this many days will be deleted
RETENTION_DAYS = 30


def create_snapshot(volume_id):
    description = f"Automated backup of {volume_id} - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"

    response = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=description,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {'Key': 'CreatedBy', 'Value': 'automated-backup-lambda'},
                    {'Key': 'SourceVolume', 'Value': volume_id}
                ]
            }
        ]
    )

    snapshot_id = response['SnapshotId']
    print(f"Created snapshot: {snapshot_id} for volume {volume_id}")
    return snapshot_id


def cleanup_old_snapshots(volume_id, retention_days):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
    deleted_snapshots = []

    # OwnerIds=['self'] ensures we only look at snapshots this account owns,
    # not public/shared snapshots - important in a shared training account.
    response = ec2.describe_snapshots(
        Filters=[
            {'Name': 'volume-id', 'Values': [volume_id]}
        ],
        OwnerIds=['self']
    )

    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime']

        if start_time < cutoff_date:
            try:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                deleted_snapshots.append(snapshot_id)
                print(f"Deleted old snapshot: {snapshot_id} (created {start_time})")
            except Exception as e:
                print(f"Could not delete snapshot {snapshot_id}: {str(e)}")

    return deleted_snapshots


def lambda_handler(event, context):
    created_snapshot_id = create_snapshot(VOLUME_ID)
    deleted_snapshot_ids = cleanup_old_snapshots(VOLUME_ID, RETENTION_DAYS)

    return {
        'created_snapshot': created_snapshot_id,
        'deleted_snapshots': deleted_snapshot_ids,
        'retention_days': RETENTION_DAYS
    }