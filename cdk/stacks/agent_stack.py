"""Agent platform stack: identity, storage, observability, API stub.

Pattern: every agent gets its own IAM role (least privilege, scoped to the
tools that agent may call). Buckets deny unencrypted uploads. Log groups
retain per-turn traces for audit and eval.
"""
from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_kms as kms,
    aws_logs as logs,
    aws_s3 as s3,
)
from constructs import Construct


class AgentPlatformStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Encryption key for data at rest ---------------------------------
        data_key = kms.Key(
            self,
            "AgentDataKey",
            description="KMS key for agent data lake buckets",
            enable_key_rotation=True,
        )

        # --- Data lake buckets (raw = immutable landing, curated = obfuscated)
        def _bucket(name: str) -> s3.Bucket:
            return s3.Bucket(
                self,
                name,
                encryption=s3.BucketEncryption.KMS,
                encryption_key=data_key,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                enforce_ssl=True,
                versioned=True,
                removal_policy=RemovalPolicy.RETAIN,
            )

        raw_bucket = _bucket("RawDataBucket")
        curated_bucket = _bucket("CuratedDataBucket")
        for bucket in (raw_bucket, curated_bucket):
            bucket.add_to_resource_policy(
                iam.PolicyStatement(
                    sid="DenyUnencryptedUploads",
                    effect=iam.Effect.DENY,
                    principals=[iam.AnyPrincipal()],
                    actions=["s3:PutObject"],
                    resources=[bucket.arn_for_objects("*")],
                    conditions={"StringNotEquals": {"s3:x-amz-server-side-encryption": "aws:kms"}},
                )
            )

        # --- Agent IAM roles: one role per agent ------------------------------
        # TODO: add one role per agent; scope each policy to that agent's tools.
        agent_role = iam.Role(
            self,
            "ExampleAgentRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            description="EXAMPLE: per-agent role. Duplicate per agent, scope tightly.",
        )
        curated_bucket.grant_read(agent_role)
        agent_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=["*"],  # TODO: scope to approved model ARNs
            )
        )

        # Human-in-the-loop approval role: the agent may REQUEST this role's
        # actions through an approval workflow, but never assumes it directly.
        approver_role = iam.Role(
            self,
            "ApproverRole",
            assumed_by=iam.AccountPrincipal(Stack.of(self).account),
            description="Held by humans; agent requests actions, humans approve.",
        )

        # --- Observability ----------------------------------------------------
        logs.LogGroup(
            self,
            "AgentTurnLogGroup",
            retention=logs.RetentionDays.THREE_MONTHS,
            removal_policy=RemovalPolicy.RETAIN,
        )

        # --- API Gateway stub -------------------------------------------------
        api = apigw.RestApi(
            self,
            "AgentApi",
            description="Front door: auth, throttling, WAF attach here.",
            deploy_options=apigw.StageOptions(
                throttling_rate_limit=100,
                throttling_burst_limit=50,
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=False,  # never log bodies; may contain PII
            ),
        )
        ask = api.root.add_resource("ask")
        ask.add_method("POST")  # TODO: attach Lambda integration + authorizer

        # Helpful outputs for wiring up the rest of the platform
        self.agent_role_arn = agent_role.role_arn
