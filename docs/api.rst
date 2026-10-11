Library API
===========

Both language implementations provide the following operations. Return values
are ordinary objects/dictionaries, arrays/lists or strings; there is no network
client or database connection.

.. list-table:: Query operations
   :header-rows: 1
   :widths: 30 30 40

   * - Node.js
     - Python
     - Behavior
   * - ``getDataset()``
     - ``get_dataset()``
     - Copy of the complete bundled JSON object, including release metadata.
   * - ``getRecord(id)``
     - ``get_record(record_id)``
     - Exact, case-sensitive ID lookup; missing ID returns ``undefined`` or ``None``.
   * - ``listRecords({topic})``
     - ``list_records(topic=None)``
     - All records when omitted; exact topic filtering ignores case and surrounding whitespace.
   * - ``searchRecords(query)``
     - ``search_records(query)``
     - Case-insensitive substring search of descriptive fields. Blank query returns no matches.
   * - ``listTopics()``
     - ``list_topics()``
     - Unique topic labels in sorted order.
   * - ``listSources()``
     - ``list_sources()``
     - Source entries with ``url`` and the associated ``record_ids``.
   * - ``formatRecordValue(record)``
     - ``format_record_value(record)``
     - Scalar, lower-bound or range text with its unit retained.
   * - ``getCitation()``
     - ``get_citation()``
     - Preferred release citation with the archived dataset DOI.
   * - ``validateDataset(dataset)``
     - ``validate_dataset(dataset=None)``
     - Structural validation result; omission uses the bundled release.

Search covers ID, topic, geography, period, entity, unit and caveat. It does not
search the source website or fetch new records. It is substring matching, not
full-text relevance ranking or semantic retrieval.

Example: filter and preserve context
--------------------------------------------

.. code-block:: javascript

   import {listRecords, listSources} from "lunarness-fashion-data";

   const rows = listRecords({topic: "ecommerce"});
   const sourceLedger = listSources();
   const output = rows.map(({id, value, unit, period, source, caveat}) => ({
     id, value, unit, period, source, caveat
   }));

.. code-block:: python

   from lunarness_fashion_data import list_records, list_sources

   rows = list_records(topic="ecommerce")
   source_ledger = list_sources()
   output = [
       {key: row.get(key) for key in ("id", "value", "unit", "period", "source", "caveat")}
       for row in rows
   ]

This example selects a topic whose records use scalar values. For arbitrary
records, inspect all supported value representations as described in
:doc:`records`; selecting only ``value`` would lose lower bounds and ranges.

Copies and mutation
-------------------

The query helpers return defensive copies. Modifying a returned record does
not change the package's bundled release. To validate an edited copy, obtain
it through ``getDataset()`` or ``get_dataset()`` and pass it explicitly to the
validator. The functions do not save that copy for you.

Do not assume that both languages interpret every malformed input identically.
Use documented argument types, omit optional filters when unused, and validate
custom data before formatting it.
