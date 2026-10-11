Record formats and interpretation
=================================

The package API returns the JSON release, whose top-level fields include
``name``, ``version``, ``published``, ``canonical_url``, ``license``, ``method``
and ``records``. A record retains its ``id``, ``topic``, ``geography``, ``period``,
``entity``, ``unit`` and supporting ``source`` URL. ``caveat`` and ``derivation``
add interpretation and calculation context where available.

Three value representations
---------------------------

.. list-table:: Preserve the representation
   :header-rows: 1
   :widths: 30 35 35

   * - Shape
     - Fields
     - Interpretation
   * - Scalar
     - ``value``
     - One reported or derived number.
   * - Lower bound
     - ``value_lower_bound``
     - A stated lower bound; retain the plus sign when formatted.
   * - Interval
     - ``value_min`` and ``value_max``
     - A range; keep both endpoints and do not invent a midpoint.

Use ``formatRecordValue`` / ``format_record_value`` for display. Keep the
underlying numeric shape when exporting or calculating. These functions retain
units but do not turn one type of metric into another.

JSON and CSV names
------------------

The repository's flattened CSV/data dictionary uses names such as ``metric_id``,
``source_url`` and ``comparability_note``. The software's bundled JSON uses
``id``, ``source`` and ``caveat``. They are different representations of the
research release; do not pass a raw CSV row to an API expecting the JSON schema
or assume that the two tables have identical row granularity.

Before mapping a CSV export, inspect its header, value encoding and the
repository's ``data_dictionary.md``. Preserve the raw source URL, period and
measurement definition during transformation. The structural validator is
documented in :doc:`validation`.

Comparability checks
--------------------

Compare records only after checking their metric, geography, population,
reference period and unit. A website visit is not a unique person or purchase.
Media Impact Value is not revenue. Apparent textile consumption is not a
product-level environmental impact score. A displayed range does not justify
a point estimate.

The package contains a small, fixed historical release. It does not establish
a comprehensive or representative market sample and cannot validate a claim
about an individual product.
