import asyncio

from arp_standard_model import (
    AtomicExecuteRequest,
    AtomicExecutorExecuteAtomicNodeRunRequest,
    NodeRunState,
    NodeTypeRef,
)
from arp_template_atomic_executor.executor import AtomicExecutor


def test_execute_atomic_echo() -> None:
    executor = AtomicExecutor()
    request = AtomicExecutorExecuteAtomicNodeRunRequest(
        body=AtomicExecuteRequest(
            node_run_id="node_run_1",
            run_id="run_1",
            node_type_ref=NodeTypeRef(node_type_id="atomic.echo", version="0.1.0"),
            inputs={"ping": "pong"},
        )
    )

    result = asyncio.run(executor.execute_atomic_node_run(request))

    assert result.state == NodeRunState.succeeded
    assert result.outputs == {"echo": {"ping": "pong"}}
