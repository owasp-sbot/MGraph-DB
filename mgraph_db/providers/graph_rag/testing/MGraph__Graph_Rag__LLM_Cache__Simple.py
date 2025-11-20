MGraph__Graph_Rag__LLM_Cache__Simple = {
    'cyber-news-1': { 'choices': [ { 'finish_reason': 'function_call',
                 'index': 0,
                 'logprobs': None,
                 'message': { 'content': None,
                              'function_call': { 'arguments': '{"entities":[{"name":"BuildFlow","primary_domains":["Development","Automation"],"functional_roles":["Continuous '
                                                              'Integration '
                                                              'Tool","Automation '
                                                              'Framework"],"ecosystem":{"platforms":["Cloud"],"standards":["CI/CD","Agile"]},"direct_relationships":[{"entity":"Continuous '
                                                              'Integration","relationship_type":"is '
                                                              'a type '
                                                              'of","strength":0.8},{"entity":"Machine '
                                                              'Learning","relationship_type":"utilizes","strength":0.7},{"entity":"Development '
                                                              'Team","relationship_type":"develops","strength":0.9}],"domain_relationships":[{"concept":"Continuous '
                                                              'Integration","relationship_type":"related '
                                                              'to","category":"Methodology","strength":0.8},{"concept":"Automation","relationship_type":"related '
                                                              'to","category":"Process","strength":0.7},{"concept":"Innovation","relationship_type":"enhances","category":"Business","strength":0.6}],"confidence":0.95},{"name":"Continuous '
                                                              'Integration","primary_domains":["Development","Software '
                                                              'Engineering"],"functional_roles":["Development '
                                                              'Methodology","Process"],"ecosystem":{"platforms": ["Various"],"standards":["CI/CD"]},"direct_relationships":[{"entity":"BuildFlow","relationship_type":"implemented '
                                                              'by","strength":0.8},{"entity":"Development '
                                                              'Team","relationship_type":"utilizes","strength":0.9}],"domain_relationships":[{"concept":"Software '
                                                              'Development","relationship_type":"part '
                                                              'of","category":"Process","strength":0.8},{"concept":"Quality '
                                                              'Assurance","relationship_type":"supports","category":"Process","strength":0.6}],"confidence":0.9},{"name":"Machine '
                                                              'Learning","primary_domains":["Artificial '
                                                              'Intelligence","Data '
                                                              'Science"],"functional_roles":["Algorithm","Data '
                                                              'Processing","Optimization '
                                                              'Technique"],"ecosystem":{"platforms": ["Various"],"standards":["ML '
                                                              'Standards","Data '
                                                              'Processing '
                                                              'Standards"],"technologies":["Python","TensorFlow","Scikit-learn"]},"direct_relationships":[{"entity":"BuildFlow","relationship_type":"enhances","strength":0.7}],"domain_relationships":[{"concept":"Artificial '
                                                              'Intelligence","relationship_type":"subfield '
                                                              'of","category":"Science","strength":0.9},{"concept":"Data '
                                                              'Analysis","relationship_type":"related '
                                                              'to","category":"Methodology","strength":0.8}],"confidence":0.93},{"name":"Development '
                                                              'Team","primary_domains":["Development","Project '
                                                              'Management"],"functional_roles":["Project '
                                                              'Implementers","Software '
                                                              'Developers"],"ecosystem":{"platforms":["Agile"],"standards":["Agile","SCRUM"]},"direct_relationships":[{"entity":"BuildFlow","relationship_type":"implements","strength":0.9},{"entity":"Continuous '
                                                              'Integration","relationship_type":"practices","strength":0.8}],"domain_relationships":[{"concept":"Team '
                                                              'Collaboration","relationship_type":"important '
                                                              'for","category":"Methodology","strength":0.7},{"concept":"Software '
                                                              'Development '
                                                              'Life '
                                                              'Cycle","relationship_type":"part '
                                                              'of","category":"Process","strength":0.8}],"confidence":0.91}]}',
                                                 'name': 'extract_entities'},
                              'refusal': None,
                              'role': 'assistant'}}],
  'created': 1738156356,
  'id': 'chatcmpl-Av29s26ZT9z2ktYXcf4ye92YplDRH',
  'model': 'gpt-4o-mini-2024-07-18',
  'object': 'chat.completion',
  'service_tier': 'default',
  'system_fingerprint': 'fp_72ed7ab54c',
  'usage': { 'completion_tokens': 598,
             'completion_tokens_details': { 'accepted_prediction_tokens': 0,
                                            'audio_tokens': 0,
                                            'reasoning_tokens': 0,
                                            'rejected_prediction_tokens': 0},
             'prompt_tokens': 403,
             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
             'total_tokens': 1001}},




    'cyber-news-2': { 'choices': [ { 'finish_reason': 'function_call',
                 'index': 0,
                 'logprobs': None,
                 'message': { 'content': None,
                              'function_call': { 'arguments': '{"entities":[{"name":"Software '
                                                              'Development '
                                                              'Standards '
                                                              'Organization","primary_domains":["Standards","Software '
                                                              'Development"],"functional_roles":["Standards '
                                                              'Body","Guidelines '
                                                              'Developer"],"ecosystem":{"standards":["Microservice '
                                                              'Architecture '
                                                              'Standards"]},"direct_relationships":[{"entity":"microservice '
                                                              'architecture","relationship_type":"develops '
                                                              'guidelines '
                                                              'for","strength":0.9}],"domain_relationships":[{"concept":"microservices","relationship_type":"related '
                                                              'to","category":"Architecture","strength":0.8},{"concept":"best '
                                                              'practices","relationship_type":"establishes","category":"Implementation '
                                                              'Methodologies","strength":0.7}],"confidence":0.95},{"name":"microservice '
                                                              'architecture","primary_domains":["Software '
                                                              'Architecture","Development"],"functional_roles":["Architectural '
                                                              'Pattern"],"ecosystem":{"technologies":["Docker","Kubernetes","Spring '
                                                              'Boot"]},"direct_relationships":[{"entity":"Software '
                                                              'Development '
                                                              'Standards '
                                                              'Organization","relationship_type":"guidelines '
                                                              'influenced '
                                                              'by","strength":0.9},{"entity":"best '
                                                              'practices","relationship_type":"involves","strength":0.8}],"domain_relationships":[{"concept":"microservices","relationship_type":"subtype '
                                                              'of","category":"Service-Oriented '
                                                              'Architecture","strength":0.9},{"concept":"deployment","relationship_type":"concerns","category":"Software '
                                                              'Development","strength":0.7}],"confidence":0.93},{"name":"best '
                                                              'practices","primary_domains":["Quality '
                                                              'Assurance","Software '
                                                              'Development"],"functional_roles":["Implementation '
                                                              'Guidelines"],"ecosystem":{"standards":["Quality '
                                                              'Standards"]},"direct_relationships":[{"entity":"microservice '
                                                              'architecture","relationship_type":"applies '
                                                              'to","strength":0.8},{"entity":"Software '
                                                              'Development '
                                                              'Standards '
                                                              'Organization","relationship_type":"established '
                                                              'by","strength":0.7}],"domain_relationships":[{"concept":"guidelines","relationship_type":"related '
                                                              'to","category":"Standards","strength":0.8},{"concept":"challenges","relationship_type":"addresses","category":"Implementation","strength":0.6}],"confidence":0.90}]}',
                                                 'name': 'extract_entities'},
                              'refusal': None,
                              'role': 'assistant'}}],
  'created': 1738156288,
  'id': 'chatcmpl-Av28m8jhuB0iXLQ5Z6ZUweildXkTO',
  'model': 'gpt-4o-mini-2024-07-18',
  'object': 'chat.completion',
  'service_tier': 'default',
  'system_fingerprint': 'fp_72ed7ab54c',
  'usage': { 'completion_tokens': 411,
             'completion_tokens_details': { 'accepted_prediction_tokens': 0,
                                            'audio_tokens': 0,
                                            'reasoning_tokens': 0,
                                            'rejected_prediction_tokens': 0},
             'prompt_tokens': 384,
             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
             'total_tokens': 795}} ,




    'cyber-news-3': { 'choices': [ { 'finish_reason': 'function_call',
                 'index': 0,
                 'logprobs': None,
                 'message': { 'content': None,
                              'function_call': { 'arguments': '{"entities":[{"name":"DevTools '
                                                              'Pro","primary_domains":["Security","Development"],"functional_roles":["Tool"],"ecosystem":{"platforms":["DevTools"],"standards":[],"technologies":[]},"direct_relationships":[{"entity":"authentication '
                                                              'system","relationship_type":"addresses","strength":0.9},{"entity":"vulnerabilities","relationship_type":"related '
                                                              'to","strength":0.8}],"domain_relationships":[{"concept":"authentication '
                                                              'protocol","relationship_type":"implementing","category":"Protocol","strength":0.75},{"concept":"security '
                                                              'researcher ABC '
                                                              'XYZ","relationship_type":"identified","category":"Individual","strength":0.7}],"confidence":0.95},{"name":"Authentication '
                                                              'System","primary_domains":["Security"],"functional_roles":["System"],"ecosystem":{"platforms":[],"standards":[],"technologies":[]},"direct_relationships":[{"entity":"DevTools '
                                                              'Pro","relationship_type":"critical '
                                                              'for","strength":0.9},{"entity":"vulnerabilities","relationship_type":"contains","strength":0.85}],"domain_relationships":[{"concept":"authentication '
                                                              'protocol","relationship_type":"designed '
                                                              'for","category":"Protocol","strength":0.8}],"confidence":0.9},{"name":"Vulnerabilities","primary_domains":["Security"],"functional_roles":["Risk"],"ecosystem":{"platforms":[],"standards":[],"technologies":[]},"direct_relationships":[{"entity":"DevTools '
                                                              'Pro","relationship_type":"addressed '
                                                              'by","strength":0.8},{"entity":"authentication '
                                                              'system","relationship_type":"influences","strength":0.85}],"domain_relationships":[{"concept":"unauthorized '
                                                              'access","relationship_type":"leads '
                                                              'to","category":"Threat","strength":0.9}],"confidence":0.9},{"name":"Authentication '
                                                              'Protocol","primary_domains":["Security"],"functional_roles":["Protocol"],"ecosystem":{"platforms":[],"standards":[],"technologies":[]},"direct_relationships":[{"entity":"authentication '
                                                              'system","relationship_type":"implemented '
                                                              'in","strength":0.75},{"entity":"security '
                                                              'researcher ABC '
                                                              'XYZ","relationship_type":"analyzes","strength":0.7}],"domain_relationships":[{"concept":"core '
                                                              'authentication '
                                                              'system","relationship_type":"represents","category":"System","strength":0.7}],"confidence":0.85},{"name":"Security '
                                                              'Researcher ABC '
                                                              'XYZ","primary_domains":["Security"],"functional_roles":["Researcher"],"ecosystem":{"platforms":[],"standards":[],"technologies":[]},"direct_relationships":[{"entity":"vulnerabilities","relationship_type":"identified","strength":0.8},{"entity":"authentication '
                                                              'protocol","relationship_type":"analyzes","strength":0.7}],"domain_relationships":[{"concept":"security '
                                                              'update","relationship_type":"works '
                                                              'on","category":"Process","strength":0.6}],"confidence":0.8}]}',
                                                 'name': 'extract_entities'},
                              'refusal': None,
                              'role': 'assistant'}}],
  'created': 1738156080,
  'id': 'chatcmpl-Av25QjaMfKY6NGJJxKuSXBO9JvyYy',
  'model': 'gpt-4o-mini-2024-07-18',
  'object': 'chat.completion',
  'service_tier': 'default',
  'system_fingerprint': 'fp_72ed7ab54c',
  'usage': { 'completion_tokens': 580,
             'completion_tokens_details': { 'accepted_prediction_tokens': 0,
                                            'audio_tokens': 0,
                                            'reasoning_tokens': 0,
                                            'rejected_prediction_tokens': 0},
             'prompt_tokens': 398,
             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
             'total_tokens': 978}} ,



    'pytest': { 'choices': [ { 'finish_reason': 'function_call',
                 'index': 0,
                 'logprobs': None,
                 'message': { 'content': None,
                              'function_call': { 'arguments': '{"entities":[{"name":"Pytest","primary_domains":["Development","Testing"],"functional_roles":["Testing '
                                                              'Framework","Tool"],"ecosystem":{"platforms":["Python"],"standards":["PEP '
                                                              '8","PEP '
                                                              '257"],"technologies":["Python","Unit '
                                                              'Tests","Integration '
                                                              'Tests"]},"direct_relationships":[{"entity":"Python","relationship_type":"uses","strength":0.9},{"entity":"Unit '
                                                              'Tests","relationship_type":"supports","strength":0.8},{"entity":"Integration '
                                                              'Tests","relationship_type":"supports","strength":0.8}],"domain_relationships":[{"concept":"Testing","relationship_type":"part '
                                                              'of","category":"Software '
                                                              'Quality","strength":0.9},{"concept":"Continuous '
                                                              'Integration","relationship_type":"related '
                                                              'to","category":"Development '
                                                              'Practices","strength":0.7}],"confidence":0.95}]}',
                                                 'name': 'extract_entities'},
                              'refusal': None,
                              'role': 'assistant'}}],
  'created': 1738155848,
  'id': 'chatcmpl-Av21gKhGXqMWchzajVDNbke1p8nDd',
  'model': 'gpt-4o-mini-2024-07-18',
  'object': 'chat.completion',
  'service_tier': 'default',
  'system_fingerprint': 'fp_72ed7ab54c',
  'usage': { 'completion_tokens': 178,
             'completion_tokens_details': { 'accepted_prediction_tokens': 0,
                                            'audio_tokens': 0,
                                            'reasoning_tokens': 0,
                                            'rejected_prediction_tokens': 0},
             'prompt_tokens': 350,
             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
             'total_tokens': 528}}
}

mgraph_llm_cache_simple = MGraph__Graph_Rag__LLM_Cache__Simple