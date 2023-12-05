EXTRACT_PARAMETES_PROMPT="""
As a text parameter matcher, your job is to install the function parameter requirements from the text to extract the corresponding parameters.
1. You need to read and understand the following text(input_text):
2. Extract the corresponding content from the text according to the following parameter information:
3. Follow these steps:

- First, read and understand the text carefully.
   - Second, look for the appropriate content in the text based on the parameter information provided.
   - Next, generate a parameter reference dictionary based on what you find. If you don't find a match for a parameter in the text, leave it blank in the dictionary.

Perform the preceding steps in sequence and generate a dictionary of parameter parameters.

Textual content (input_text):
[insert text content here]

Parameter information (parameter_info):
[insert parameter info here]

Generated parameter reference dictionary:
[Generate a parameter reference dictionary here, and if the corresponding value cannot be matched, an empty dictionary will be generated]
"""
EXTRACT_PARAMETES_EXAMPLE_PROMPT="""
Here is some examples

Textual content (input_text):
"Alice, who is 25 years old, works at Acme Corp. Her email is alice@example.com."

Parameter information (parameter_info):
[{'name': 'name', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The name of this people.', 'properties': None, 'items': None}},{'name': 'age', 'required': True, 'parameter_schema': {'type': 'int', 'description': 'The age of this people.', 'properties': None, 'items': None}},{'name': 'email', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The email of this people.', 'properties': None, 'items': None}}]

Generated parameter reference dictionary:
{"name": "Alice", "age": 25, "email": "alice@example.com"}

Textual content (input_text):
"The weather in Paris is mostly sunny this week, with a high of 18°C and a low of 7°C."

Parameter information (parameter_info):
[{'name': 'w', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'What kind of weather?', 'properties': None, 'items': None}},{'name': 'age', 'required': True, 'parameter_schema': {'type': 'int', 'description': 'The age of this people.', 'properties': None, 'items': None}},{'name': 'email', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The email of this people.', 'properties': None, 'items': None}}]

Generated parameter reference dictionary:
{"w": "sunny"}

Textual content (input_text):
"This new novel is thrilling and full of unexpected twists."

Parameter information (parameter_info):
[{'name': 'x', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'input x content', 'properties': None, 'items': None}},{'name': 'age', 'required': True, 'parameter_schema': {'type': 'int', 'description': 'The age of this people.', 'properties': None, 'items': None}},{'name': 'email', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The email of this people.', 'properties': None, 'items': None}}]

Generated parameter reference dictionary:
{}
"""
EXTRACT_PARAMETES_HINT="""
Please provide the information in dictionary format. Make sure that the name of each parameter appears as a key, and extract its matching information from the text as the corresponding value.
"""