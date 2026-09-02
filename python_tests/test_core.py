import json
import unittest
from copy import deepcopy
from pathlib import Path

from lunarness_fashion_data import (
    format_record_value,
    get_citation,
    get_dataset,
    get_record,
    list_records,
    list_sources,
    list_topics,
    search_records,
    validate_dataset,
)


class CoreTests(unittest.TestCase):
    def test_packaged_dataset_matches_canonical_file(self):
        canonical = json.loads(
            (Path(__file__).parents[1] / "data" / "fashion_observatory_2026.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(get_dataset(), canonical)

    def test_loads_complete_versioned_dataset(self):
        dataset = get_dataset()
        self.assertEqual(dataset["version"], "1.0")
        self.assertEqual(len(dataset["records"]), 10)

    def test_returns_defensive_copies(self):
        dataset = get_dataset()
        dataset["records"][0]["entity"] = "Changed"
        self.assertNotEqual(get_dataset()["records"][0]["entity"], "Changed")

    def test_filters_finds_and_searches(self):
        self.assertEqual(len(list_records("ecommerce")), 2)
        self.assertEqual(get_record("eu_textile_consumption")["value"], 19)
        self.assertIsNone(get_record("missing"))
        self.assertGreaterEqual(len(search_records("textile")), 2)
        self.assertEqual(search_records(""), [])

    def test_lists_unique_topics_and_sources(self):
        self.assertEqual(len(list_topics()), 5)
        self.assertEqual(len(list_sources()), 9)

    def test_formats_all_value_shapes(self):
        self.assertEqual(format_record_value({"value": 19, "unit": "kg"}), "19 kg")
        self.assertEqual(
            format_record_value({"value_lower_bound": 184, "unit": "visits"}),
            "184+ visits",
        )
        self.assertEqual(
            format_record_value({"value_min": 2, "value_max": 8, "unit": "percent"}),
            "2–8 percent",
        )

    def test_validates_bundled_dataset(self):
        result = validate_dataset()
        self.assertTrue(result["valid"])
        self.assertEqual(result["stats"]["records"], 10)

    def test_rejects_duplicates_and_incomplete_ranges(self):
        candidate = deepcopy(get_dataset())
        candidate["records"][1]["id"] = candidate["records"][0]["id"]
        candidate["records"][2].pop("value")
        candidate["records"][2]["value_min"] = 4
        result = validate_dataset(candidate)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Duplicate record id" in error for error in result["errors"]))
        self.assertTrue(any("value_min and value_max together" in error for error in result["errors"]))

    def test_returns_stable_doi_citation(self):
        self.assertIn("10.5281/zenodo.22131190", get_citation())


if __name__ == "__main__":
    unittest.main()
