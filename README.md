# Agentic AI on AWS — Production Reference Architecture

A reference architecture for building **production-ready AI agents on AWS**,
distilled from patterns used across enterprise AI/ML engagements: agent identity
and access control, the model lifecycle, regression testing for AI applications,
data preparation for cloud onboarding, and governance/observability.

> **Reference, not production code.** The CDK stacks and tests here are starter
> skeletons showing the patterns. Harden them for your environment before use.

## Architecture

```
                ┌─────────────────────────────────────────────┐
                │                  AWS Account                 │
                │                                              │
  Users ──▶ API Gateway ──▶ Lambda (orchestrator)              │
                              │                                │
                              ▼                                │
                    ┌─────────────────────┐                    │
                    │  Bedrock AgentCore   │                    │
                    │  (agent runtime)     │                    │
                    │  w/ IAM agent roles  │◀── IAM identity    │
                    └─────────┬───────────┘   per agent         │
                              │                                │
              ┌───────────────┼────────────────┐               │
              ▼               ▼                ▼               │
        Bedrock models   S3 (data lake,    CloudWatch          │
        (versioned,       KMS-encrypted)    (logs, metrics,    │
         evaluated)                         traces)            │
                              │                                │
                    ┌─────────▼───────────┐                    │
                    │ Regression tests    │                    │
                    │ (Playwright, in     │                    │
                    │  CI pipeline)        │                    │
                    └─────────────────────┘                    │
└─────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full write-up.

## Repo map

| Path | What it is |
|---|---|
| `docs/architecture.md` | Full architecture write-up: components, identity model, lifecycle, testing, governance |
| `cdk/` | AWS CDK (Python) starter skeleton: agent IAM roles, encrypted S3, log groups, API Gateway stub |
| `tests/` | Playwright regression-test skeleton for an AI app endpoint |
| `CONTRIBUTING.md` | How to extend this reference |

## Patterns covered

1. **Agent identity** — every agent runs under its own IAM role; no shared credentials, least-privilege policies scoped per tool/action.
2. **Model lifecycle** — versioned model IDs, evaluation gates before promotion, rollback path.
3. **Regression testing** — Playwright suites in CI that assert on agent behavior (latency budgets, refusal behavior, schema-valid outputs), not just HTTP 200s.
4. **Data obfuscation for cloud onboarding** — PII/PHI tokenization and masking before data lands in the cloud data lake.
5. **Governance & observability** — structured logging, traces per agent turn, cost and quality dashboards.

## Quick start

```bash
cd cdk
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk synth        # inspect the template
cdk deploy       # deploys the skeleton into your account
```

## License

MIT — see [LICENSE](LICENSE).
