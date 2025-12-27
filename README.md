# ARP Template Atomic Executor

Use this repo as a starting point for building an **ARP compliant Atomic Executor** service.

This minimal template implements the Atomic Executor API using only the SDK packages:
`arp-standard-server`, `arp-standard-model`, and `arp-standard-client`.

It is intentionally small and readable so you can replace the handler logic with your own domain capabilities while keeping the same API surface.

Implements: ARP Standard `spec/v1` Atomic Executor API (contract: `ARP_Standard/spec/v1/openapi/atomic-executor.openapi.yaml`).

## Requirements

- Python >= 3.10

## Install

```bash
python3 -m pip install -e .
```

## Local configuration (optional)

For local dev convenience, copy the template env file:

```bash
cp .env.example .env.local
```

`src/scripts/dev_server.sh` auto-loads `.env.local` (or `.env`).

## Run

- Atomic Executor listens on `http://127.0.0.1:8082` by default.

```bash
python3 -m pip install -e '.[run]'
python3 -m arp_template_atomic_executor
```

> [!TIP]
> Use `bash src/scripts/dev_server.sh --host ... --port ... --reload` for dev convenience.

## Using this repo

To build your own executor, fork this repository and replace/add handlers while preserving request/response semantics.

If all you need is to change what atomic node types do, edit:
- `src/arp_template_atomic_executor/executor.py`

### Default behavior

- Implements a single deterministic handler: `atomic.echo`.
- `execute_atomic_node_run` returns `succeeded` with `outputs={"echo": inputs}` for `atomic.echo`.
- Unknown `node_type_id` returns `failed` with an error payload.

## Quick health check

```bash
curl http://127.0.0.1:8082/v1/health
```

## Configuration

CLI flags:
- `--host` (default `127.0.0.1`)
- `--port` (default `8082`)
- `--reload` (dev only)

## Validate conformance (`arp-conformance`)

```bash
python3 -m pip install arp-conformance
arp-conformance check atomic-executor --url http://127.0.0.1:8082 --tier smoke
arp-conformance check atomic-executor --url http://127.0.0.1:8082 --tier surface
```

## Helper scripts

- `src/scripts/dev_server.sh`: run the server (flags: `--host`, `--port`, `--reload`).
- `src/scripts/send_request.py`: execute an atomic NodeRun from a JSON file.

  ```bash
  python3 src/scripts/send_request.py --request src/scripts/request.json
  ```

## Authentication

For out-of-the-box usability, this template defaults to auth-disabled unless you set `ARP_AUTH_MODE` or `ARP_AUTH_PROFILE`.

To enable JWT auth, set either:
- `ARP_AUTH_PROFILE=dev-secure-keycloak` + `ARP_AUTH_SERVICE_ID=<audience>`
- or `ARP_AUTH_MODE=required` with `ARP_AUTH_ISSUER` and `ARP_AUTH_AUDIENCE`

## Upgrading

When upgrading to a new ARP Standard SDK release, bump pinned versions in `pyproject.toml` (`arp-standard-*==...`) and re-run conformance.
