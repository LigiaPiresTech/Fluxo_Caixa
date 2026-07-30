import json
import logging
from typing import Any

logger = logging.getLogger("audit")

def audit_event(
    event_type: str,
    user_id: str | None,
    entity: str,
    entity_id: str | None,
    action: str,
    metadata: dict[str, Any] | None = None,
):
    # Application/business audit event.
    # Technical logs go to CloudWatch; financial audit records should also be
    # persisted in HISTORICOS_LANCAMENTOS/LOGS as required by the business.
    logger.info(json.dumps({
        "event_type": event_type,
        "user_id": user_id,
        "entity": entity,
        "entity_id": entity_id,
        "action": action,
        "metadata": metadata or {},
    }, ensure_ascii=False))
