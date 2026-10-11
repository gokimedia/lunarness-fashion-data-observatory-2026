Installation and first query
============================

Node.js
-------

Use Node.js 18 or newer. The package is an ES module and has no runtime npm
dependencies. Pin the release when reproducing an analysis:

.. code-block:: console

   npm install lunarness-fashion-data@1.0.0
   npx lunarness-fashion-data validate --json

Query a record while keeping its context:

.. code-block:: javascript

   import {getRecord, formatRecordValue} from "lunarness-fashion-data";

   const record = getRecord("eu_textile_consumption");
   if (record !== undefined) {
     console.log(formatRecordValue(record));
     console.log(record.period, record.geography);
     console.log(record.caveat, record.source);
   }

The bundled record reports ``19 kg per capita``, for EU27 in 2022, with the
caveat ``Apparent consumption estimate``. This is an example of querying a
published historical record, not a new observation or a live estimate.

Python
------

Use Python 3.9 or newer, preferably inside a virtual environment:

.. code-block:: console

   python -m venv .venv

Activate the virtual environment using your operating system's normal
procedure, then install the pinned package:

.. code-block:: console

   python -m pip install lunarness-fashion-data==1.0.0

In your application:

.. code-block:: python

   from lunarness_fashion_data import get_record, format_record_value

   record = get_record("eu_textile_consumption")
   if record is not None:
       print(format_record_value(record))
       print(record["period"], record["geography"])
       print(record.get("caveat"), record["source"])

No API key is required. Queries use the locally bundled JSON, so changes to the
public website do not change an installed package. Upgrade deliberately and
record both the package and dataset versions.

Troubleshooting
---------------

If an import fails, check the active environment and the installed package
name. The Python import uses underscores: ``lunarness_fashion_data``. If a CLI
command comes from the wrong implementation, check your executable path or
call the Node CLI through ``npx`` in its project directory.
