
# Automated Instance Management Using AWS Lambda and Boto3
A hands on AWS Serverless &amp; Cloud Automation repo showcasing real-world automation projects using AWS Lambda, Boto3, IAM, EventBridge, CloudWatch and Python. Covers cost optimization, infrastructure automation, event-driven workflows, and production-ready serverless patterns through assignments, reusable code, and step-by-step implementations.
## Objective
Automate stopping and starting of EC2 instances based on tags, using an AWS Lambda function written in Python with Boto3.

## Architecture
- Two EC2 instances, each tagged with key `Action`
  - `Action = Auto-Stop` → instance should be stopped when the Lambda runs
  - `Action = Auto-Start` → instance should be started when the Lambda runs
- One Lambda function (`ec2-auto-stop-start`) that:
  - Describes instances filtered by `tag:Action` and `instance-state-name`
  - Stops all running `Auto-Stop` tagged instances
  - Starts all stopped `Auto-Start` tagged instances
  - Logs affected instance IDs to CloudWatch Logs
- One IAM role (`lambda-ec2-tag-manager-role`) with the `AmazonEC2FullAccess` managed policy, attached as the Lambda execution role

## Steps Followed

### 1. EC2 Setup
- Launched two `t3.micro` (free tier eligible) instances in `us-west-1`
  - `vikramjeet-ec1` → tagged `Action = Auto-Stop`, kept **running**
  - `vikramjeet-ec2` → tagged `Action = Auto-Start`, manually **stopped**
- Screenshot: `screenshots/Launch-an-instance-EC2-us-west-1-08-02-2026_07_10_PM.png`

### 2. IAM Role for Lambda
- Created an IAM role via IAM → Roles → Create role
  - Trusted entity: AWS service → Lambda
  - Permissions policy: `AmazonEC2FullAccess` (AWS managed)
  - Role name: `lambda-ec2-tag-manager-role`
- Screenshot: `screenshots/lambda-ec2-tag-manager-role-IAM-Global-08-02-2026_07_13_PM.png`

> Note: `AmazonEC2FullAccess` is used here for simplicity as required by the assignment.
> In a production setting this would be replaced with a least-privilege custom policy scoped to `ec2:DescribeInstances`, `ec2:StopInstances`, and `ec2:StartInstances` only.

### 3. Lambda Function
- Created function `ec2-auto-stop-start`
  - Runtime: Python 3.14
  - Execution role: existing role → `lambda-ec2-tag-manager-role`
- Replaced the default handler code with `lambda_function.py` (included in this repo)
- Deployed the function
- Screenshot: `screenshots/Create-function-Functions-Lambda-08-02-2026_07_09_PM.png`

### 4. Manual Invocation / Testing
- Created a test event (`manualTest`) with default JSON payload (event data is not used by this function)
- Invoked the function via the **Test** tab
- Result:
  ```json
  {
    "stopped": ["i-06678126d09b1d022"],
    "started": ["i-0da61b135f3ff7079"]
  }
  ```
- CloudWatch logs confirmed:
  ```
  Stopped instances: ['i-06678126d09b1d022']
  Started instances: ['i-0da61b135f3ff7079']
  ```
- Screenshot: `screenshots/ec2-auto-stop-start-Functions-Lambda-Test-Run-08-02-2026_07_09_PM.png`

### 5. Verification
- Confirmed in the EC2 console that:
  - `vikramjeet-ec1` (Auto-Stop) transitioned to **stopped**
  - `vikramjeet-ec2` (Auto-Start) transitioned to **running**
- Screenshot: `screenshots/instances_state_after_test_run.png`

## Code
See `lambda_function.py` for the full Boto3 script.

## Result
The Lambda function correctly identifies EC2 instances by tag and state, then stops/starts them accordingly, with full logging for traceability. Manual invocation confirmed expected behavior end to end.