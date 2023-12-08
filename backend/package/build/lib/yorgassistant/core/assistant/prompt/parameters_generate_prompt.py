PARAMETERS_GENERATE_PROMPT = """
As a tool's parameters generator, you'll generate tool parameters. Depending on the provided tool name (tool_name), tool summary (tool_summary), user input (input_text) and tool input schema (tool_input_schema), you'll need to follow these steps:

1. Read and understand the tool summary (tools_summary):
    - Understand the functionality, features, and limitations of the tool.

2. Analyze User Input (input_text):
    - Understand the user's needs or problems.
    - Identify keywords or phrases to determine which parameters need to be generated.

3. Analyze tool input schema:
    - Understand the schema of the tool input.
    - Identify the parameters that need to be generated.

4. Output:
    - Generate the parameters that need to be generated as json format.
    - If no parameters need to be generated, the output is empty string.

Note that the generation of tool parameters should be based on the user's needs and refer to the tool summary and tool input schema provided. Follow the steps above and make sure to provide accurate tool parameters in the output.
"""

PARAMETERS_GENERATE_EXAMPLE_PROMPT = """
Here is some examples about parameters generating:

Input:
tool_name: "code interpreter"
tool_summary: "Run the code through code_interpreter and return a dictionary including a log of the code run and whether it was successful or not."
input_text: "Tell me the 17th Fibonacci number."
tool_input_schema: [
    \{
    "name": "code",
    "description": "code text that requires code_interpreter to run",
    "required": true,
    "schema": {
        "type": "string"
    }
\}
]

Output:
\{
"code": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n-1):\n        a, b = b, a + b\n    return a\n\nprint(fibonacci(17))",
\}
"""

PARAMETERS_GENERATE_HINT = """
You should only output the json string of parameters, such as {"code": "print('Hello World')"}. Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
"""