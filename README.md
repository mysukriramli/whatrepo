# API Drift Preemption Wire

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Autonomous Machine Feed](https://img.shields.io/badge/Feed-Autonomous_6h-blue.svg)](data/today.json)

An autonomous contract-breakage radar engineered for **AI coding agents (Cursor, Devin, Copilot), integration-maintenance bots, and platform engineering pipelines**.

The wire monitors active OpenAPI specifications from primary cloud services (GitHub, OpenAI, Stripe, Resend, PostHog), runs semantic diffs on endpoints and parameter requirements, correlates changes against public SDK release dates (PyPI/npm), and emits deterministic failover directives before production code breaks.

---

## 📡 Live Machine Endpoints (Zero-Auth / Fastly Edge CDN)

| Endpoint | Format | Consumer Purpose |
| :--- | :--- | :--- |
| [`data/today.json`](data/today.json) | JSON | Active API drift scores and machine directives across tracked services. |
| [`data/remediation_queue.jsonl`](data/remediation_queue.jsonl) | JSONL | Streaming queue for CI/CD test generation and automated PR builders. |
| [`data/llms.txt`](data/llms.txt) | Markdown | Token-efficient digest for Cursor and LLM prompt context injection. |
| `data/archive/YYYY/MM/` | JSON | Permanent historical log of upstream API breaking-change timelines. |

---

## 🤖 Directives Emitted

- `GENERATE_COMPATIBILITY_SHIM`: Critical endpoint removal or new required parameter; generate local adapter shim.
- `PIN_SDK`: Upstream schema has mutated breaking contracts while official SDK has not released an update; pin current version.
- `REGENERATE_CLIENT`: Schema updated with active SDK release; re-run openapi-generator.
- `ADD_CONTRACT_TEST`: Non-critical schema variance; inject mock contract test into test suite.
- `SAFE_TO_UPGRADE`: Zero breaking changes detected; fully backward-compatible.
