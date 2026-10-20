"""Target-specific credential custody contract; no secret retrieval implemented."""
from __future__ import annotations

from typing import Protocol


class CredentialProvider(Protocol):
    """Resolve a target-bound ephemeral credential without exposing its value."""

    def acquire(self, target_id: str, operator_identity: str) -> object: ...
    def release(self, handle: object) -> None: ...


class CredentialProviderUnavailable(RuntimeError):
    pass


class NoCredentialProvider:
    def acquire(self, target_id: str, operator_identity: str) -> object:
        raise CredentialProviderUnavailable("HOLD: CIO-approved credential provider is not configured")

    def release(self, handle: object) -> None:
        raise CredentialProviderUnavailable("HOLD: no credential provider owns this handle")
