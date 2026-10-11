Validation and release integrity
================================

``validateDataset`` / ``validate_dataset`` checks structure and a limited set
of interpretation-sensitive invariants. Its result has ``valid``, ``errors``,
``warnings`` and ``stats``. ``valid`` depends on the absence of errors; it does
not require an empty warnings list.

Checks in version 1.0.0
------------------------------

- Required release and record fields are present.
- ``records`` is a nonempty collection of objects.
- IDs are unique and source/canonical URLs use HTTPS.
- Values are finite numbers with exactly one supported representation.
- Range endpoints occur together and the minimum does not exceed the maximum.
- A missing caveat produces a warning for review.

The validator does not fetch source URLs, establish reuse rights, reproduce
third-party measurements, compare HTTP responses, or independently certify
accuracy. A public URL can become unavailable while the bundled release still
passes a structural check.

Current observed result
-----------------------

The published npm and PyPI 1.0.0 artifacts were checked on October 11, 2026.
Both returned 10 JSON records, 5 topics and 9 source URLs, with no structural
errors. Both also returned warnings for these records:

- ``eu_online_apparel_age_gap``: no caveat.
- ``eu_textile_waste``: no caveat.

These warnings are retained here; this documentation does not silently repair
or relabel a previously published dataset. Review the observation and its
supporting source before reusing it.

Validate a modified copy
------------------------

.. code-block:: python

   from lunarness_fashion_data import get_dataset, validate_dataset

   candidate = get_dataset()
   candidate["records"][0]["source"] = "http://example.invalid/"
   result = validate_dataset(candidate)
   assert result["valid"] is False
   assert result["errors"]

.. code-block:: javascript

   import {getDataset, validateDataset} from "lunarness-fashion-data";

   const candidate = getDataset();
   candidate.records[0].source = "http://example.invalid/";
   const result = validateDataset(candidate);
   console.assert(result.valid === false);

These examples modify an in-memory copy. They make no HTTP request and do not
change the installed release.

When updating documentation
---------------------------

Record the package version, dataset version, artifact checksums and relevant
source review date. Re-run examples against the released packages. A source
correction should be made transparently in the project's normal release
workflow, with its citation and caveats maintained.
