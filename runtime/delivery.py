"""Explicit delivery authorization for scheduled runtime jobs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryPolicy:
    destination: str
    production: bool = False
    require_explicit_approval: bool = True

    def authorize(self, *, approved: bool = False) -> str:
        """Return the destination only when the policy permits delivery."""
        if not self.destination.strip():
            raise ValueError("destination must not be empty")
        if self.require_explicit_approval and not approved:
            raise PermissionError("explicit delivery approval is required")
        if self.production and not approved:
            raise PermissionError("production delivery requires approval")
        return self.destination
