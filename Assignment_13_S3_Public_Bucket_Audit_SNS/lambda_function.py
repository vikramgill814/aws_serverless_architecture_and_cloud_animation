import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

# Replace with your actual SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:975050024946:s3-public-bucket-alert'


def is_bucket_public(bucket_name):
    """Check both Block Public Access settings and the bucket policy/ACL."""

    # 1. Check the Block Public Access configuration first.
    # If all 4 settings are True, the bucket is protected regardless of policy/ACL.
    try:
        pab = s3.get_public_access_block(Bucket=bucket_name)
        config = pab['PublicAccessBlockConfiguration']
        fully_blocked = all([
            config.get('BlockPublicAcls', False),
            config.get('IgnorePublicAcls', False),
            config.get('BlockPublicPolicy', False),
            config.get('RestrictPublicBuckets', False)
        ])
        if fully_blocked:
            return False
    except s3.exceptions.ClientError:
        # No Block Public Access configuration set at all -> treat as not blocked
        pass

    # 2. Check bucket policy for public principal ("*")
    try:
        policy_response = s3.get_bucket_policy(Bucket=bucket_name)
        policy = json.loads(policy_response['Policy'])
        for statement in policy.get('Statement', []):
            principal = statement.get('Principal')
            if principal == '*' or (isinstance(principal, dict) and principal.get('AWS') == '*'):
                if statement.get('Effect') == 'Allow':
                    return True
    except s3.exceptions.ClientError:
        # No bucket policy exists - not an error, just means no policy-based public access
        pass

    # 3. Check bucket ACL for public grants
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        for grant in acl.get('Grants', []):
            grantee = grant.get('Grantee', {})
            uri = grantee.get('URI', '')
            if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                return True
    except s3.exceptions.ClientError:
        pass

    return False


def lambda_handler(event, context):
    buckets = s3.list_buckets()['Buckets']
    print(f"Total buckets found: {len(buckets)}")
    public_buckets = []

    for bucket in buckets:
        name = bucket['Name']
        try:
            if is_bucket_public(name):
                public_buckets.append(name)
            print(f"Checked bucket: {name}")
        except Exception as e:
            print(f"Could not evaluate bucket {name}: {str(e)}")

    if public_buckets:
        message = "The following S3 buckets are PUBLICLY accessible:\n\n" + "\n".join(public_buckets)
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="AWS Alert: Public S3 Bucket(s) Detected",
            Message=message
        )
        print(f"Public buckets found and alert sent: {public_buckets}")
    else:
        print("No public buckets found. All buckets are private.")

    return {
        'public_buckets': public_buckets
    }