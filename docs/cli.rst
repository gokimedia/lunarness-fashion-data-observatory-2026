Command-line interface
======================

The Node.js and Python distributions install an executable named
``lunarness-fashion-data``. The following command shapes are shared:

.. code-block:: console

   lunarness-fashion-data list [--topic TOPIC] [--json]
   lunarness-fashion-data get RECORD_ID [--json]
   lunarness-fashion-data search QUERY [--json]
   lunarness-fashion-data topics [--json]
   lunarness-fashion-data sources [--json]
   lunarness-fashion-data validate [--json]
   lunarness-fashion-data citation
   lunarness-fashion-data --version

For Node.js, prefix a command with ``npx`` from the project in which the package
is installed. Quote multiword search text when using a shell:

.. code-block:: console

   npx lunarness-fashion-data search "Fashion Week" --json
   npx lunarness-fashion-data list --topic ecommerce --json
   npx lunarness-fashion-data get eu_textile_consumption --json

For an activated Python environment, the equivalent commands start directly
with ``lunarness-fashion-data``. JSON mode is useful for scripts; human-readable
table layout differs between the language implementations.

Exit status
-----------

Successful commands return status 0. An unknown record ID returns status 1.
Usage errors, such as a missing required record ID, return status 2. A failed
structural validation returns status 1; validation warnings alone do not change
the successful status. Check the JSON ``warnings`` list instead of discarding it.

``--version`` reports the software distribution version. The dataset release
version appears in ``getDataset()`` / ``get_dataset()`` and is a separate value.

The executable reads bundled data; it neither downloads updated source pages
nor accepts an arbitrary external dataset path. Use the library validator for
your own edited dataset objects.
