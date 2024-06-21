"""
Module for middleware models
"""

from dataclasses import dataclass
import datetime
import uuid


@dataclass(frozen=True)
class UsagePayload:
    """
    Model for Usage record.
    """

    product_id: uuid.UUID
    tenant_id: uuid.UUID
    memory_mb: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    workflow: str
    id: uuid.UUID = uuid.uuid4()
    owner_id: str = None
    duration: float = None
    created_at: str = datetime.datetime.utcnow().isoformat()

    def jsonable_dict(self):
        return {
            "id": str(self.id),  # noqa: F821
            "product_id": str(self.product_id),
            "tenant_id": str(self.tenant_id),
            "memory_mb": self.memory_mb,
            "start_timestamp": str(self.start_time),
            "end_timestamp": str(self.end_time),
            "workflow": self.workflow,
            "owner_id": self.owner_id,
            "duration": self.duration,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class AuditPayload:
    """
    Model for Audit record.
    """

    id: str
    url: str
    method: str
    client_ip: str
    status_code: int
    tenant_id: str
    sub: str
    process_time: str
    created_at: str = datetime.datetime.utcnow().isoformat()
