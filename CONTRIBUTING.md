# Contributing

This is a reference architecture, not a product. Contributions that sharpen
the patterns are welcome:

- **New patterns** — add a section to `docs/architecture.md` describing a
  production problem, the AWS-native pattern that solves it, and the
  trade-offs. Real-world grounding beats theory.
- **CDK extensions** — extend `cdk/stacks/agent_stack.py` (new constructs for
  eval pipelines, VPC endpoints, WAF rules). Keep the "one role per agent"
  identity model intact.
- **Tests** — add Playwright specs under `tests/` that assert on agent
  *behavior* (refusals, budgets, schema validity), not exact text.

Please don't submit client-specific code or anything you don't have the
rights to share. Open an issue first for larger changes.
