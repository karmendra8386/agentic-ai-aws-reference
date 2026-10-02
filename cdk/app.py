#!/usr/bin/env python3
"""CDK app: starter skeleton for the agentic-AI-on-AWS reference architecture.

Deploys: agent IAM roles, KMS-encrypted S3 buckets, CloudWatch log groups,
and an API Gateway stub. This is scaffolding — extend with your agent
runtime, tools, and policies.
"""
import aws_cdk as cdk

from stacks.agent_stack import AgentPlatformStack

app = cdk.App()

AgentPlatformStack(
    app,
    "AgentPlatformStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1",
    ),
    description="Starter scaffolding: IAM agent roles, encrypted S3, logs, API stub",
)

app.synth()
