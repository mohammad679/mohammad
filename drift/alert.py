from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def trigger_alert(message: str, webhook_url: str = "") -> None:
    if webhook_url:
        logger.warning("Slack webhook placeholder configured; skipping external call.", extra={"webhook": webhook_url})
    logger.warning("Drift alert triggered", extra={"alert_message": message})
