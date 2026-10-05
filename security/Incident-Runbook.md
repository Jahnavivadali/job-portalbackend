# Security Incident Runbook – Suspicious Root Login

## 1. Purpose

This runbook describes the steps to detect, investigate, contain, and recover from a suspicious AWS root account login. It uses AWS CloudTrail to record account activity and Amazon CloudWatch alarms to identify potential security incidents.

## 2. Incident Scenario

A root account console login is detected in AWS CloudTrail. The CloudWatch alarm `CloudTrail-Root-Login-Alarm` is configured to trigger when the `RootLoginCount` metric reaches or exceeds 1 within a five-minute period.

A root login is not automatically malicious, but unexpected or unauthorized root account activity must be investigated immediately.

## 3. Services Involved

* **AWS CloudTrail:** Records AWS account activity and console login events.
* **Amazon CloudWatch Logs:** Stores CloudTrail event logs.
* **Amazon CloudWatch Alarms:** Detects root login events using a metric filter.
* **AWS IAM:** Helps review account access and credentials.
* **AWS WAF:** Provides web application traffic protection where applicable.

## 4. Incident Detection

1. Open the AWS Management Console.
2. Navigate to Amazon CloudWatch in the configured AWS Region.
3. Open **Alarms** and locate `CloudTrail-Root-Login-Alarm`.
4. Check whether the alarm has entered the ALARM state.
5. Open the CloudTrail log group `/aws/cloudtrail/multi-region-security-trail`.
6. Search for the `ConsoleLogin` event and inspect the event details.

## 5. Investigation

1. Record the event time, AWS Region, source IP address, and user identity.
2. Verify whether the login was performed by an authorized administrator.
3. Check the CloudTrail event's `responseElements.ConsoleLogin` value, when available, to determine whether the login succeeded.
4. Review nearby CloudTrail events for unexpected IAM changes, access key creation, security group changes, or other suspicious actions.
5. Preserve relevant logs and document the findings.
6. If the activity cannot be verified, treat it as a potential security incident and escalate it to the responsible account administrator or security team.

## 6. Containment

1. Contact the authorized AWS account owner or security administrator immediately.
2. If unauthorized access is suspected, secure the root account using the official AWS account recovery and security procedures.
3. Change the root password if compromise is suspected and secure the account's MFA configuration.
4. Review and remove unauthorized IAM users, access keys, roles, or policies after confirming they are malicious.
5. Revoke suspicious temporary sessions or credentials where applicable.
6. Avoid deleting logs or making changes that could destroy evidence.

## 7. Recovery

1. Confirm that the root account and affected IAM identities are secured.
2. Verify that MFA is enabled for the root account.
3. Review IAM permissions and apply least-privilege access.
4. Check for unauthorized resources or configuration changes and remediate them.
5. Confirm that CloudTrail is logging across all required Regions and that log file validation remains enabled.
6. Verify that the CloudWatch metric filter and root-login alarm are configured correctly.
7. Monitor account activity for further suspicious events.

## 8. Communication and Documentation

Record the incident date and time, event details, investigation results, containment actions, recovery steps, and final outcome. Notify the account owner and relevant security stakeholders. Follow the organization's incident reporting and escalation procedures.

## 9. Prevention

* Enable and maintain MFA for the root account.
* Avoid using the root account for routine administrative work.
* Use IAM roles and least-privilege permissions for normal operations.
* Keep multi-Region CloudTrail logging and log file validation enabled.
* Monitor root login and security group change alarms.
* Review AWS account activity and security configurations regularly.

## 10. Completion Criteria

The incident can be closed when the login has been investigated, the account is secured, unauthorized changes have been remediated, required logs have been preserved, and monitoring is functioning correctly.

**Note:** This runbook is a response guide for the project. Actual containment actions must be performed by an authorized AWS account administrator based on the investigation findings.
