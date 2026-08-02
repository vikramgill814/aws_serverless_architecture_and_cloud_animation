# AWS Serverless Architecture and Cloud Automation

A hands-on repository of AWS automation projects built with **AWS Lambda, Boto3, IAM, Amazon EventBridge, Amazon SNS, and CloudWatch**. Each folder is a self-contained assignment covering a different serverless automation pattern — cost optimization, security auditing, backup automation, and event-driven monitoring.

## Repository Structure

```
aws_serverless_architecture_and_cloud_animation/
├── assignment-1-ec2-auto-stop-start/
│   ├── README.md
│   ├── lambda_function.py
│   └── screenshots/
├── Assignment_13_S3_Public_Bucket_Audit_SNS/
│   ├── README.md
│   ├── lambda_function.py
│   └── screenshots/
├── Assignment4_EBS_Snapshot_backup_plus_cleanup_automation/
│   ├── README.md
│   ├── lambda_function.py
│   └── screenshots/
├── EC2_State_Change_EventBridge_plus_SNS/
│   ├── README.md
│   ├── lambda_function.py
│   └── screenshots/
└── submission.txt
```

Each assignment folder contains:
- **`README.md`** — objective, architecture, step-by-step process followed, troubleshooting notes, and results (with screenshots)
- **`lambda_function.py`** — the full Boto3 script deployed to AWS Lambda
- **`screenshots/`** — console screenshots documenting each step

## Assignments Summary

### 1. [EC2 Auto Stop/Start](./assignment-1-ec2-auto-stop-start)
A Lambda function that stops and starts EC2 instances automatically based on tags (`Action=Auto-Stop` / `Action=Auto-Start`). Demonstrates IAM execution roles, tag-based filtering with Boto3, and idempotent automation (only acting on instances in the "wrong" state).

**Services used:** Lambda, EC2, IAM

### 2. [S3 Public Bucket Audit + SNS Alert](./Assignment_13_S3_Public_Bucket_Audit_SNS)
A Lambda function that audits every S3 bucket in the account for public accessibility (checking Block Public Access settings, bucket policies, and ACLs) and sends an SNS email alert listing any exposed buckets. Includes real troubleshooting of a Lambda timeout caused by a 43-bucket shared account.

**Services used:** Lambda, S3, SNS, IAM

### 3. [EBS Snapshot Backup + Cleanup](./Assignment4_EBS_Snapshot_backup_plus_cleanup_automation)
A Lambda function that creates a tagged, timestamped EBS snapshot on each run and automatically deletes snapshots older than a 30-day retention window — a simple automated backup rotation pattern.

**Services used:** Lambda, EBS (EC2 API), IAM

### 4. [EC2 State Change Notification via EventBridge + SNS](./EC2_State_Change_EventBridge_plus_SNS)
An event-driven pipeline: an EventBridge rule detects EC2 instance state changes (start/stop/terminate) in real time and automatically invokes a Lambda function, which sends an SNS email alert — no manual invocation required. Unlike the other assignments, this Lambda consumes data directly from the triggering event rather than querying AWS APIs itself.

**Services used:** Lambda, EventBridge, EC2, SNS, IAM

## Key Concepts Demonstrated Across Assignments
- **IAM execution roles** — least-privilege-style permission attachment for Lambda (S3 read-only, EC2 full access, SNS publish, etc.), and troubleshooting `AccessDenied` errors from missing/incorrect roles
- **Manually-invoked vs. event-driven Lambdas** — Assignments 1, 4, and 13 use manually-triggered Lambdas that query AWS APIs; Assignment 14 uses a fully event-driven EventBridge → Lambda pipeline
- **SNS pub/sub notifications** — email alerting for security findings, backup status, and infrastructure state changes
- **Lambda timeout tuning** — diagnosing and fixing a real `Sandbox.Timedout` error caused by looping over many AWS resources
- **Tag-based resource targeting** — using EC2 tags to drive automation logic instead of hardcoded resource IDs
- **Multi-region considerations** — working across `us-west-1` (EC2/EBS resources) and `us-east-1` (where billing/some services are region-locked)

## Environment
- AWS Account: shared academic/training account
- Regions used: `us-west-1` (EC2, EBS, EventBridge), `us-east-1` (S3 audit, SNS for Assignment 13)
- Runtime: Python 3.14 (AWS Lambda)
- SDK: Boto3
