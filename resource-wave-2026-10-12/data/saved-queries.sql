-- Literal metadata indicators; not verified adjustment ranges or fit recommendations.
SELECT COUNT(*) AS snapshot_records FROM catalog_signals;

SELECT product_type, COUNT(*) AS records,
       SUM(numeric_unit_pair) AS numeric_unit_signal_records,
       SUM(numeric_range_with_unit) AS literal_range_signal_records
FROM catalog_signals GROUP BY product_type ORDER BY records DESC, product_type;

SELECT handle, source_url, unit_tokens_detected
FROM catalog_signals
WHERE numeric_unit_pair = 1 AND numeric_range_with_unit = 0
ORDER BY handle;

SELECT handle, source_url
FROM catalog_signals
WHERE size_option_name = 1 AND numeric_unit_pair = 0
ORDER BY handle;

-- Run on a Dolt database after a later captured snapshot is committed:
-- SELECT * FROM dolt_log;
-- SELECT * FROM dolt_diff_catalog_signals;
