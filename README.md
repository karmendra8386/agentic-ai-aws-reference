# Agentic AI on AWS — Production Reference Architecture

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23178788.svg)](https://doi.org/10.5281/zenodo.23178788)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A reference architecture for building **production-ready AI agents on AWS**,
distilled from patterns used across enterprise AI/ML engagements: agent identity
and access control, the model lifecycle, regression testing for AI applications,
data preparation for cloud onboarding, and governance/observability.

> **Reference, not production code.** The CDK stacks and tests here are starter
> skeletons showing the patterns. Harden them for your environment before use.

## Research

This implementation accompanies the paper:

**Karmendra Pandey. "From Pilots to Production: A Reference Architecture for
Cost-Governed AI Agents on AWS."** Zenodo, 2026.
DOI: [10.5281/zenodo.23178788](https://doi.org/10.5281/zenodo.23178788)

- Submitted to the ICSE 2027 Software Engineering in Practice (SEIP) track.
- Submitted to the IEEE Software special issue on Building Trustworthy Software
  in the Time of AI (Jul/Aug 2027).

If you use this work, please cite:

```bibtex
@misc{pandey2026pilots,
  author       = {Karmendra Pandey},
  title        = {From Pilots to Production: A Reference Architecture for
                  Cost-Governed AI Agents on AWS},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23178788},
  url          = {https://doi.org/10.5281/zenodo.23178788}
}
```

Related writing: [Your AI Agent Has a Burn Rate](https://dev.to/karmendra_pandey_43ac6983/your-ai-agent-has-a-burn-rate-governing-the-cost-of-production-ai-agents-on-aws-1jil)
(dev.to) · [I Found a Cost Blind Spot in an Open-Source Agent Framework](https://dev.to/karmendra_pandey_43ac6983/i-found-a-cost-blind-spot-in-an-open-source-agent-framework-34b9)
(dev.to)

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

## Author

**Karmendra Pandey** — Practice Architect, AI & ML Practice, TEK Systems.
ORCID: [0009-0000-3461-9889](https://orcid.org/0009-0000-3461-9889) ·
[LinkedIn](https://www.linkedin.com/in/karmendra-pandey-79126b9)

## License

MIT — see [LICENSE](LICENSE).
