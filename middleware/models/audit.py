"""
Model for Audit record.
"""

from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class AuditPayload:
    id: str
    url: str
    method: str
    client_ip: str
    status_code: int
    tenant_id: str
    user_id: str
    process_time: str
    created_at: str = datetime.datetime.utcnow().isoformat()
