import json
from build_catalog_signals import signals, text_only

assert signals('Ships in seven days',[])['numeric_unit_pair']==0
assert signals('Ships in 7 days',[])['numeric_unit_pair']==0
assert signals('Length: 12 inches',[])['numeric_unit_pair']==1
assert signals('Width: 2.5 cm',[])['numeric_range_with_unit']==0
assert signals('Adjustment: 28–34 cm',[])['numeric_range_with_unit']==1
assert signals('Adjustment: 28 to 34 cm',[])['numeric_range_with_unit']==1
assert signals('Two parts: 28 and 34 cm',[])['numeric_range_with_unit']==0
assert signals('Width: 2,5cm',[])['numeric_unit_pair']==1
assert signals('Length: 30 mm',[])['unit_tokens_detected']=='mm'
assert signals('Model name X12cmA',[])['numeric_unit_pair']==0
assert signals('<script>12 cm buckle waist</script><p>paper</p>',[])['numeric_unit_pair']==0
assert signals('Ties at the waist',[])['closure_token']==1
assert signals('Elastic metal mesh',[])['material_token']==1
assert signals('No dimensions here',[' Color ',' Size '])['size_option_name']==1
assert signals('No dimensions here',['Sizing Notes'])['size_option_name']==0
assert text_only('<p>A&nbsp;B</p><p>C</p>')=='A B C'
print(json.dumps({'meaningful_rule_scenarios_passed':16, 'scope':'literal indicators only; no inferred dimensions or product-quality scores'}))
