lunarness-fashion-data documentation
============================================

``lunarness-fashion-data`` is an existing, zero-dependency Node.js and Python
package for querying a bundled release of the Lunarness Fashion Data Observatory.
It exposes record lookup, topic filtering, text search, source grouping and
structural validation without scraping a live website.

This documentation targets package version **1.0.0**. The dataset's own release
version is **1.0**, published August 27, 2026. They are separate version fields.

The `canonical Observatory page
<https://lunarness.com/pages/fashion-statistics-observatory>`_ explains the
dataset's measurement context. The `public source repository
<https://github.com/gokimedia/lunarness-fashion-data-observatory-2026>`_ contains
the implementations, data, tests and release metadata. This guide documents
those existing tools; it does not announce a new dataset or software package.

.. toctree::
   :maxdepth: 2
   :caption: Using the package

   quickstart
   api
   cli
   records
   validation
   citation

Choose the Node.js or Python instructions according to your application. Both
publish the same CLI executable name, so avoid installing their executables
into the same environment unless you know which one is on your path.

Limits of the release
---------------------

A structurally valid record is not an independently verified fact. Preserve
its period, geography, unit, source and caveat when displaying it. Media Impact
Value is not sales or revenue; historical attendance observations are not a
current standardized ranking. Product sustainability, safety and medical
claims are outside this project's scope.
