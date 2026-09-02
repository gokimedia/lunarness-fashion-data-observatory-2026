"""Query and validate the bundled Lunarness fashion dataset."""

from __future__ import annotations

import json
from copy import deepcopy
from importlib.resources import files
from math import isfinite
from typing import Any, Dict, List, Mapping, Optional
from urllib.parse import urlparse


_DATA_PATH = files("lunarness_fashion_data").joinpath(
    "data/fashion_observatory_2026.json"
)
with _DATA_PATH.open("r", encoding="utf-8") as _stream:
    _BUNDLED_DATASET: Dict[str, Any] = json.load(_stream)

_REQUIRED_DATASET_FIELDS = (
    "name",
    "version",
    "published",
    "canonical_url",
    "license",
    "records",
)
_REQUIRED_RECORD_FIELDS = (
    "id",
    "topic",
    "geography",
    "period",
    "entity",
    "unit",
    "source",
)
_VALUE_FIELDS = ("value", "value_lower_bound", "value_min", "value_max")


def _normalize(value: Any) -> str:
    return str(value if value is not None else "").strip().casefold()


def _is_https_url(value: Any) -> bool:
    try:
        parsed = urlparse(str(value))
    except (TypeError, ValueError):
        return False
    return parsed.scheme == "https" and bool(parsed.netloc)


def get_dataset() -> Dict[str, Any]:
    """Return a defensive copy of the complete bundled dataset."""

    return deepcopy(_BUNDLED_DATASET)


def list_records(topic: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return all records, optionally filtered by exact topic."""

    records = _BUNDLED_DATASET["records"]
    if topic is not None:
        records = [row for row in records if _normalize(row.get("topic")) == _normalize(topic)]
    return deepcopy(records)


def get_record(record_id: str) -> Optional[Dict[str, Any]]:
    """Return one record by ID, or ``None`` when it does not exist."""

    for record in _BUNDLED_DATASET["records"]:
        if record.get("id") == record_id:
            return deepcopy(record)
    return None


def search_records(query: str) -> List[Dict[str, Any]]:
    """Case-insensitively search the descriptive fields of every record."""

    needle = _normalize(query)
    if not needle:
        return []
    fields_to_search = (
        "id",
        "topic",
        "geography",
        "period",
        "entity",
        "unit",
        "caveat",
    )
    matches = [
        record
        for record in _BUNDLED_DATASET["records"]
        if any(needle in _normalize(record.get(field)) for field in fields_to_search)
    ]
    return deepcopy(matches)


def list_topics() -> List[str]:
    """Return the unique topic names in stable sorted order."""

    return sorted({record["topic"] for record in _BUNDLED_DATASET["records"]})


def list_sources() -> List[Dict[str, Any]]:
    """Group record IDs by their supporting source URL."""

    sources: Dict[str, List[str]] = {}
    for record in _BUNDLED_DATASET["records"]:
        sources.setdefault(record["source"], []).append(record["id"])
    return [
        {"url": url, "record_ids": deepcopy(sources[url])}
        for url in sorted(sources)
    ]


def format_record_value(record: Mapping[str, Any]) -> str:
    """Format scalar, lower-bound and range records without changing meaning."""

    unit = record.get("unit", "")
    if isinstance(record.get("value"), (int, float)):
        return f"{record['value']} {unit}".strip()
    if isinstance(record.get("value_lower_bound"), (int, float)):
        return f"{record['value_lower_bound']}+ {unit}".strip()
    if isinstance(record.get("value_min"), (int, float)) and isinstance(
        record.get("value_max"), (int, float)
    ):
        return f"{record['value_min']}–{record['value_max']} {unit}".strip()
    return f"Unspecified {unit}".strip()


def get_citation() -> str:
    """Return the preferred short citation for the dataset release."""

    year = str(_BUNDLED_DATASET["published"])[:4]
    return (
        f"Lunarness Editorial Team ({year}). {_BUNDLED_DATASET['name']} "
        f"(Version {_BUNDLED_DATASET['version']}). "
        "https://doi.org/10.5281/zenodo.22131190"
    )


def validate_dataset(dataset: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    """Validate structural and interpretation-sensitive dataset invariants."""

    candidate: Any = _BUNDLED_DATASET if dataset is None else dataset
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(candidate, Mapping):
        return {
            "valid": False,
            "errors": ["Dataset must be a JSON object."],
            "warnings": warnings,
            "stats": {"records": 0, "topics": 0, "sources": 0},
        }

    for field in _REQUIRED_DATASET_FIELDS:
        if candidate.get(field) in (None, ""):
            errors.append(f"Dataset is missing required field: {field}.")

    if not _is_https_url(candidate.get("canonical_url")):
        errors.append("Dataset canonical_url must be a valid HTTPS URL.")

    raw_records = candidate.get("records")
    records = raw_records if isinstance(raw_records, list) else []
    if not isinstance(raw_records, list):
        errors.append("Dataset records must be an array.")
    if not records:
        errors.append("Dataset must contain at least one record.")

    identifiers = set()
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            errors.append(f"record[{index}] must be an object.")
            continue
        label = record.get("id") or f"record[{index}]"
        for field in _REQUIRED_RECORD_FIELDS:
            if record.get(field) in (None, ""):
                errors.append(f"{label} is missing required field: {field}.")

        record_id = record.get("id")
        if record_id:
            if record_id in identifiers:
                errors.append(f"Duplicate record id: {record_id}.")
            identifiers.add(record_id)

        if not _is_https_url(record.get("source")):
            errors.append(f"{label} source must be a valid HTTPS URL.")

        present = [field for field in _VALUE_FIELDS if field in record]
        has_scalar = "value" in present
        has_lower_bound = "value_lower_bound" in present
        has_min = "value_min" in present
        has_max = "value_max" in present
        if not (has_scalar or has_lower_bound or (has_min and has_max)):
            errors.append(
                f"{label} must define value, value_lower_bound, or both value_min and value_max."
            )
        if has_min != has_max:
            errors.append(f"{label} must define value_min and value_max together.")
        if (has_scalar and len(present) > 1) or (has_lower_bound and len(present) > 1):
            errors.append(f"{label} mixes incompatible value representations.")

        for field in present:
            value = record[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
                errors.append(f"{label} {field} must be a finite number.")
        if has_min and has_max and record["value_min"] > record["value_max"]:
            errors.append(f"{label} value_min cannot exceed value_max.")
        if not record.get("caveat"):
            warnings.append(
                f"{label} has no caveat; confirm that the metric cannot be misread."
            )

    topics = {record.get("topic") for record in records if isinstance(record, Mapping) and record.get("topic")}
    sources = {record.get("source") for record in records if isinstance(record, Mapping) and record.get("source")}
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "records": len(records),
            "topics": len(topics),
            "sources": len(sources),
        },
    }
