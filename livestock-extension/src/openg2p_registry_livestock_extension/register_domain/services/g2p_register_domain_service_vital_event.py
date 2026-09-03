import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_int, ear_tag_exists, is_blank, parse_date, validate_species_matches, validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")

# field -> human label used in the "Please provide the ... " message, mirroring
# the fields marked "widget-required" on the Vital Event Details form.
_REQUIRED_FIELDS = {
    "ear_tag_id": "livestock ear tag",
    "species": "species",
    "event_type": "event type",
    "event_date": "event date",
}


class G2PRegisterDomainServiceVitalEvent(G2PRegisterDomainService):

    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_required_fields(record)
            await self._validate_ear_tag_exists(record)
            await validate_species_matches(record)
            self._validate_not_in_future(record, "event_date")
            self._validate_not_in_future(record, "date_onset")
            self._validate_date_order(record, "date_onset", "date_resolution")
            self._validate_offspring_count(record)

    def _validate_required_fields(self, record: dict) -> None:
        for field, label in _REQUIRED_FIELDS.items():
            if is_blank(record.get(field)):
                validation_error(f"Please provide the {label} before saving the record.")

    async def _validate_ear_tag_exists(self, record: dict) -> None:
        value = record.get("ear_tag_id")
        if value is None or str(value).strip() == "":
            return
        if not await ear_tag_exists(str(value).strip()):
            validation_error(
                "ear_tag_id does not match any registered or drafted animal. "
                "Add it under Livestock Details first, or check for a typo."
            )

    def _validate_not_in_future(self, record: dict, field: str) -> None:
        value = parse_date(record.get(field))
        if value is not None and value > date.today():
            validation_error(f"{field} must not be in the future")

    def _validate_date_order(self, record: dict, earlier: str, later: str) -> None:
        start = parse_date(record.get(earlier))
        end = parse_date(record.get(later))
        if start and end and end < start:
            validation_error(f"{later} must not be before {earlier}")

    def _validate_offspring_count(self, record: dict) -> None:
        # Only births carry offspring; a non-birth event with a count is a
        # data-entry slip worth rejecting rather than silently storing.
        count = as_int(record.get("offspring_count"))
        if count is None:
            return
        if count < 0:
            validation_error("offspring_count must not be negative")
        if count > 0 and str(record.get("event_type") or "").upper() != "BIRTH":
            validation_error("offspring_count is only valid on a BIRTH event")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for vital event record")

        keys = [
            "functional_record_id",
            "ear_tag_id",
            "species",
            "event_type",
            "cause",
            "disease_type",
            "veterinarian_name",
            "reporting_officer",
            "location",
            "location_details",
        ]
        search_text = []
        if extra:
            search_text.extend(str(item).strip() for item in extra if str(item).strip())
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(search_text).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for vital event record")

        keys = ["event_type", "ear_tag_id"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
