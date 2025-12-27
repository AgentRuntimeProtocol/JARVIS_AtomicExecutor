from __future__ import annotations

from .executor import AtomicExecutor
from .utils import auth_settings_from_env_or_dev_insecure


def create_app():
    return AtomicExecutor().create_app(
        title="ARP Template Atomic Executor",
        auth_settings=auth_settings_from_env_or_dev_insecure(),
    )


app = create_app()

