# SPIKE-M001: MCP Host-Operated and Embedded Agent Execution

**Tracker:** `RGT-S007`

**Status:** Queued. Do not execute before production tools, artifact lifecycles, long-running jobs, and security boundaries are specified well enough to expose safely.

## Question

Can RigTale support both agent-host-operated production through MCP and unattended embedded agent execution without duplicating workflows, misrepresenting subscription capabilities, weakening approval controls, or exposing secrets and projects?

## Why This Requires a Spike

MCP standardizes tool interoperability but host behavior, interactive approvals, model access, subscription policy, media handling, and long-running task support vary. Embedded execution uses different credentials and cost controls. Documentation claims must be verified against current official sources and real host behavior.

## Execution Modes

### Host-operated MCP

A compatible external host discovers and invokes scoped RigTale tools under its own user session, model availability, subscription, and approval behavior. RigTale does not receive or transform the host's subscription into reusable API credentials.

### Embedded or unattended agent

RigTale runs the production loop itself using explicitly configured provider credentials or another documented provider mechanism. It owns model routing, budgets, retries, scheduling, and operational records.

Both modes must use the same application operations, production contracts, validation, jobs, findings, and approvals.

## Preconditions

- The v1 production contracts and agent-system boundaries are reviewed.
- `RGT-D013` has approved representative application-tool schemas and the long-running-job contract.
- Representative tools exist as stable executable operations or bounded test doubles conforming to those approved schemas.
- Job polling, cancellation, artifact references, findings, and approvals have defined and testable behavior.
- Test projects contain no private credentials or restricted assets.

## Questions to Resolve

1. Which target hosts can discover and invoke local or remote MCP servers under their current product policies?
2. Which host features are available through interactive subscriptions, and which require API or separate provider credentials?
3. How do hosts handle tool approval, filesystem access, media artifacts, long jobs, reconnection, and resumed conversations?
4. Should job progress use polling, resources, notifications, or another supported mechanism per host?
5. How does a new host session resume from durable production state without hidden conversation memory?
6. Which production mutations require explicit user approval in host-operated and embedded modes?
7. How are prompt injection, malicious imported content, oversized tool results, duplicate calls, and abandoned jobs contained?
8. What common tool granularity works for both hosts and embedded orchestration without exposing raw engine controls?
9. What provider abstraction and secret model are required for unattended execution?
10. What cost, latency, reliability, and context differences materially affect production completion?

## Method

1. Verify current MCP specifications and each target host's official documentation at recorded versions or access dates.
2. Define a minimal common tool set covering read state, create bounded artifact revision, validate, submit job, inspect progress, record finding, and request approval.
3. Implement or simulate the same operations behind MCP and an embedded adapter without changing production artifacts.
4. Execute a bounded production workflow in every available target host and embedded provider configuration.
5. Test tool discovery, structured errors, duplicate requests, cancellation, process restart, host reconnection, and session replacement.
6. Test text, structured artifacts, images or preview references, and outputs too large for one tool response.
7. Introduce malicious instructions inside scripts, asset metadata, web research, and rendered-text content.
8. Record subscription, credential, approval, cost, context, time, and feature limitations precisely.
9. Extend evaluation to a representative multi-stage production segment and measure human interventions.

## Measurements

- valid tool-call and artifact rate;
- approval prompts and required human interventions;
- duplicate or abandoned job incidence;
- reconnection and cross-session resume success;
- tool-result size and media-transfer behavior;
- context, latency, retries, provider cost, and completion rate;
- secret exposure and prompt-injection test outcomes;
- unsupported host feature count and fallback quality; and
- divergence between MCP and embedded production artifacts.

## Required Outputs

- Source-cited capability matrix for each evaluated host and embedded provider path.
- Exact host, client, protocol, server, model, and adapter versions where observable.
- Reproducible tool schemas, commands, projects, and run records.
- Explicit statement of what subscriptions do and do not provide.
- Recommended common application-tool boundary and host-specific compatibility policy.
- Approval, secret, job-progress, reconnect, and failure-handling requirements.
- Updates to product requirements, agent system, system design, operations, quality system, and implementation plan.
- Decision records for MCP surface and embedded execution strategy.

## Exit Criteria

- At least two relevant MCP hosts are evaluated when accessible, plus one embedded provider path.
- The same versioned production operations are exercised without format divergence.
- Long-running job and session-resume behavior is demonstrated or recorded as a blocking host limitation.
- Subscription and credential claims cite official documentation and observed behavior.
- Security and prompt-injection cases produce contained, auditable failures.
- The recommended tool boundary remains useful without exposing renderer internals.

## Rejection Conditions

- Reject any design that treats an interactive subscription as a general API key.
- Reject host-specific production formats or hidden state required to render an approved project.
- Reject tools that combine broad mutation, rendering, approval, and deletion into one unauditable call.
