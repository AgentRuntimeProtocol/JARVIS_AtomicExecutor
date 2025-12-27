from __future__ import annotations

from arp_standard_model import (
    AtomicExecuteResult,
    AtomicExecutorCancelAtomicNodeRunRequest,
    AtomicExecutorExecuteAtomicNodeRunRequest,
    AtomicExecutorHealthRequest,
    AtomicExecutorVersionRequest,
    Error,
    Health,
    NodeRunState,
    Status,
    VersionInfo,
)
from arp_standard_server.atomic_executor import BaseAtomicExecutorServer

from . import __version__
from .utils import now


class AtomicExecutor(BaseAtomicExecutorServer):
    """Atomic execution surface; implement your node logic here."""

    # Core method - API surface and main extension points
    def __init__(
        self,
        *,
        service_name: str = "arp-template-atomic-executor",
        service_version: str = __version__,
    ) -> None:
        """
        Not part of ARP spec; required to construct the executor.

        Args:
          - service_name: Name exposed by /v1/version.
          - service_version: Version exposed by /v1/version.

        Potential modifications:
          - Inject dependencies needed by your atomic handlers.
          - Add persistence or tracing helpers.
        """
        self._service_name = service_name
        self._service_version = service_version

    # Core methods - Atomic Executor API implementations
    async def health(self, request: AtomicExecutorHealthRequest) -> Health:
        """
        Mandatory: Required by the ARP Atomic Executor API.

        Args:
          - request: AtomicExecutorHealthRequest (unused).
        """
        _ = request
        return Health(status=Status.ok, time=now())

    async def version(self, request: AtomicExecutorVersionRequest) -> VersionInfo:
        """
        Mandatory: Required by the ARP Atomic Executor API.

        Args:
          - request: AtomicExecutorVersionRequest (unused).
        """
        _ = request
        return VersionInfo(
            service_name=self._service_name,
            service_version=self._service_version,
            supported_api_versions=["v1"],
        )

    async def execute_atomic_node_run(self, request: AtomicExecutorExecuteAtomicNodeRunRequest) -> AtomicExecuteResult:
        """
        Mandatory: Required by the ARP Atomic Executor API.

        Args:
          - request: AtomicExecutorExecuteAtomicNodeRunRequest with NodeRun inputs.

        Potential modifications:
          - Add routing to different handlers by node_type_id.
          - Enforce budgets/constraints before execution.
          - Emit richer outputs or artifacts.
        """
        started_at = now()
        node_type_id = request.body.node_type_ref.node_type_id
        try:
            outputs = self._handle_atomic(node_type_id, request.body.inputs)
            return AtomicExecuteResult(
                node_run_id=request.body.node_run_id,
                state=NodeRunState.succeeded,
                outputs=outputs,
                output_artifacts=None,
                started_at=started_at,
                ended_at=now(),
                error=None,
            )
        except KeyError:
            return AtomicExecuteResult(
                node_run_id=request.body.node_run_id,
                state=NodeRunState.failed,
                outputs=None,
                output_artifacts=None,
                started_at=started_at,
                ended_at=now(),
                error=Error(code="unknown_node_type", message=f"Unknown node_type_id: {node_type_id}"),
            )

    async def cancel_atomic_node_run(self, request: AtomicExecutorCancelAtomicNodeRunRequest) -> None:
        """
        Mandatory: Required by the ARP Atomic Executor API.

        Args:
          - request: AtomicExecutorCancelAtomicNodeRunRequest with node_run_id.

        Potential modifications:
          - Add cooperative cancellation to your executor implementation.
        """
        _ = request
        return None

    # Helpers (internal): implementation detail for the template.
    def _handle_atomic(self, node_type_id: str, inputs: dict[str, object]) -> dict[str, object]:
        """Minimal handler router for atomic nodes (edit/extend this)."""
        if node_type_id == "atomic.echo":
            return {"echo": inputs}
        raise KeyError(node_type_id)
