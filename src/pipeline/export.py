import logging

from apify import Actor

from ..entities import Lead

logger = logging.getLogger(__name__)


class ExportService:
    """Platform-agnostic export: push leads to dataset + charge per billable lead."""

    def __init__(self, charge_event: str = "LEAD_DISCOVERED", require_contact: bool = True):
        self.charge_event = charge_event
        self.require_contact = require_contact

    async def export(self, leads: list[Lead]) -> int:
        billable = [
            l for l in leads
            if l.qualified and (not self.require_contact or l.contact_ready)
        ]
        for lead in leads:
            await Actor.push_data(lead.to_dict())

        if billable:
            try:
                await Actor.charge(event_name=self.charge_event, count=len(billable))
                logger.info("Charged %s for %d qualified leads", self.charge_event, len(billable))
            except Exception as e:
                logger.warning("Failed to charge %s for %d leads: %s",
                               self.charge_event, len(billable), e)
        return len(billable)
