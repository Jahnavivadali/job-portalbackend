# SLI/SLO Document – Cloud Security Implementation
## Introduction

Service Level Indicators (SLIs) are measurable values used to monitor the performance, reliability, or security behavior of a service. Service Level Objectives (SLOs) define the target level that an SLI should meet over a specific period. This document defines SLIs and SLOs for AWS WAF, AWS Secrets Manager, and AWS CloudTrail used in the cloud security architecture.
## 1. AWS WAF

### SLI
Percentage of incoming web requests inspected by the AWS WAF Web ACL.

### SLO
At least 99% of incoming web requests should be inspected by the WAF Web ACL.

### Measurement
The SLI can be monitored using WAF request and logging metrics to verify that incoming application traffic is being processed by the Web ACL.
## 2. AWS Secrets Manager

### SLI
Percentage of required secret retrieval operations completed successfully by the application.

### SLO
At least 99% of required secret retrieval operations should complete successfully.

### Measurement
The SLI can be monitored using application logs, CloudWatch monitoring, and Secrets Manager activity to identify successful and failed secret retrieval operations.
## 3. AWS CloudTrail

### SLI
Percentage of required AWS management events successfully delivered to the configured CloudTrail destinations.

### SLO
At least 99% of required management events should be successfully delivered to Amazon S3 and CloudWatch Logs.

### Measurement
The SLI can be monitored by checking CloudTrail delivery status, CloudTrail logs in Amazon S3, and the CloudWatch Logs destination.
## SLI/SLO Summary

| Security Service | SLI | SLO |
|---|---|---|
| AWS WAF | Percentage of incoming web requests inspected by the Web ACL | >= 99% |
| AWS Secrets Manager | Percentage of required secret retrieval operations completed successfully | >= 99% |
| AWS CloudTrail | Percentage of required management events successfully delivered to configured destinations | >= 99% |