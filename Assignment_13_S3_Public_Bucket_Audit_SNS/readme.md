
# Assignment 13: Audit S3 Bucket Permissions and Notify for Public Buckets

**Objective:** Automatically audit S3 bucket permissions and send SNS notifications if any buckets are publicly accessible (read or write).

**Repository:**
- Code: `lambda_function.py` (in this folder)
- Screenshots: [Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots)

**Architecture (high level):**
- One Lambda function `s3-public-bucket-audit` (Python + Boto3)
- One SNS topic `s3-public-bucket-alert` (email subscription)
- One IAM role attached to the Lambda (S3 read + SNS publish + CloudWatch Logs)

**Prerequisites:**
- An AWS account with permissions to create SNS topics, Lambda functions, and IAM roles.
- Python runtime supported by Lambda (this project used Python 3.14).

**How it works (summary):**
1. Lambda lists all S3 buckets in the account.
2. For each bucket the function checks:
   - Block Public Access settings
   - Bucket policy for public principals (e.g. "Principal": "*")
   - Bucket ACLs that allow public READ/WRITE
3. Any bucket determined to be public is added to a list.
4. If one or more public buckets are found, a human-readable SNS message listing those buckets is published to the configured SNS topic.

**Files:**
- `lambda_function.py` — main function and helper checks (check Block Public Access, policy, ACL, and publish to SNS).

**Setup steps (concise):**

**1) SNS Setup**
- Create an SNS topic named `s3-public-bucket-alert` (Standard).
- Create an Email subscription for the topic and confirm it from your mailbox.

**2) Create IAM Role for Lambda**
- Create a Lambda execution role and attach these managed policies:
  - `AWSLambdaBasicExecutionRole` (for CloudWatch Logs)
  - `AmazonS3ReadOnlyAccess` (to read bucket ACLs/policies)
  - `AmazonSNSFullAccess` (or a least-privilege policy allowing `sns:Publish` to your topic)

**3) Create Lambda Function**
- Runtime: Python 3.14 (or supported runtime)
- Handler: `lambda_function.lambda_handler` (see file)
- Add the SNS Topic ARN (either as an environment variable or constant in the code).
- Increase the function timeout (example: 2 minutes) if you have many buckets.

**4) Schedule (CloudWatch Events / EventBridge)**
- Create a rule to run the Lambda daily (cron or rate expression).

**5) Testing**
- Make one or two test buckets public (policy or ACL) and run the Lambda manually from the console.
- Check CloudWatch logs for the function's execution and confirm that an SNS email was received listing public buckets.

**Code reference**
- See `lambda_function.py` in this folder for the exact Boto3 implementation used during the assignment.

**Screenshots (detailed)**

**Step 1: SNS Topic Creation**
![SNS topic creation](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/s3-public-bucket-alert-Topics-Simple-Notification-Service-us-east-1-08-02-2026_10_27_PM.png)
*SNS topic named `s3-public-bucket-alert` in the AWS console.*

**Step 2: SNS Subscription Setup**
![Subscription setup](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/Create-subscription-Subscriptions-Simple-Notification-Service-us-east-1-08-02-2026_10_30_PM.png)
*Email subscription being created for the SNS topic.*

**Step 3: Subscription Confirmation**
![Subscription confirmation](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/Subscription-confirm-08-02-2026_10_22_PM.png)
*Confirmation that the subscription was successfully created.*

**Step 4: IAM Role Creation**
![IAM role creation](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/Roles-IAM-Global-08-02-2026_10_27_PM.png)
*IAM role screen used to create the Lambda execution role.*

**Step 5: IAM Permissions**
![IAM permissions](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/s3-public-bucket-audit-role-hpzzpclq-IAM-Global-Policy-Attached-08-02-2026_10_26_PM.png)
*Attached policies for S3 read access, SNS publish access, and Lambda logging.*

**Step 6: Lambda Function Code**
![Lambda function code](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/s3-public-bucket-audit-Functions-Lambda-08-02-2026_10_23_PM.png)
*Lambda function code and configuration in the AWS console.*

**Step 7: Lambda Test Execution**
![Lambda test execution](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/s3-public-bucket-audit-Functions-Lambda-Test_creation-08-02-2026_10_23_PM.png)
*Test run and function response after execution.*

**Step 8: SNS Notification Email**
![Notification email](Assignment_13_S3_Public_Bucket_Audit_SNS/screenshots/AWS-Alert-Public-S3-Bucket-s-Detected-vikramgill814-gmail-com-Gmail-08-02-2026_10_21_PM.png)
*SNS email received for public bucket detection.*

**Troubleshooting & notes**
- If you see `AccessDenied` for `s3:ListAllMyBuckets`, ensure `AmazonS3ReadOnlyAccess` is attached to the execution role.
- For many buckets, sequential checks can time out — increase the Lambda timeout or parallelize the checks.
- To reduce false positives, check the bucket's Block Public Access configuration first — if all block settings are enabled, you can skip policy/ACL checks.

**Result**
- The Lambda completed successfully and sent an SNS email listing public buckets discovered in the account.

**Next steps (optional)**
- Convert the hardcoded SNS ARN into an environment variable for easier reuse across environments.
- Implement parallel checks using `concurrent.futures.ThreadPoolExecutor` for large accounts.
- Replace the periodic Lambda with an AWS Config managed rule for continuous evaluation.
