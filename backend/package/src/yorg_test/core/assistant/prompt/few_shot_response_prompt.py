RESPONSE_PROMPT="""
As a polite AI assistant, you need to observe the required parameter information and then ask the user questions to get the corresponding parameter information.
Please provide specific information or feedback based on the following parameter information parameter_info. Your answer should be clear and unambiguous, relevant to the information provided by the parameters, and provide appropriate details and examples.
"""

RESPONSE_EXAMPLE_PROMPT="""
Here is some examples

Parameter information (parameter_info):
[{'name': 'name', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The name of this people.', 'properties': None, 'items': None}},{'name': 'age', 'required': True, 'parameter_schema': {'type': 'int', 'description': 'The age of this people.', 'properties': None, 'items': None}},{'name': 'email', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The email of this people.', 'properties': None, 'items': None}}]

Response sentence:
To proceed, could you please provide the name, age, and email of the person in question? These details are essential for us to move forward.

Parameter information (parameter_info):
[{'name': 'w', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'What kind of weather?', 'properties': None, 'items': None}},{'name': 'age', 'required': True, 'parameter_schema': {'type': 'int', 'description': 'The age of this people.', 'properties': None, 'items': None}},{'name': 'email', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The email of this people.', 'properties': None, 'items': None}}]

Response sentence:
Could you please tell me what type of weather you are experiencing, how old the person in question is, and their email address?

Parameter information (parameter_info):
[{'name': 'x', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'input x content', 'properties': None, 'items': None}},{'name': 'age', 'required': True, 'parameter_schema': {'type': 'int', 'description': 'The age of this people.', 'properties': None, 'items': None}},{'name': 'email', 'required': True, 'parameter_schema': {'type': 'string', 'description': 'The email of this people.', 'properties': None, 'items': None}}]

Response sentence:
Could you please provide the content for 'x' (a string input), the age of the person involved (an integer), and their email address (a string input)?
"""

RESPONSE_PROMPT_HINT = """
please output a sentence to user.
The goal is for the user to answer based on the parameters
"""