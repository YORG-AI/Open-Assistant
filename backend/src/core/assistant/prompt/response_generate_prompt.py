RESPONSE_GENERATE_PROMPT = """
As a response generator, you'll provide users with suggestions on response generation. Depending on the provided user input (input_text), chosen tool infomation (chosen_tool_info), tool input (tool_input),  tool result (tool_result) , you'll need to follow these steps:

1. Read and understand the chosen tool infomation (chosen_tool_info):
    - Understand the functionality, feature of the chosen tool.

2. Analyze user input and tool input and result:
    - Understand the user's needs or problems.
    - Understand the tool input generate by LLM and tool result generate by tool.

3. Output:
    - Rearrange the tool's result, make it more readable and understandable.
    - Generate the response that need to be generated as string format.

Note that the generation of response should be based on the user's needs and refer to the chosen tool infomation provided. Follow the steps above and make sure to provide accurate response in the output.
"""

RESPONSE_GENERATE_EXAMPLE_PROMPT = """
Here is some examples about response generating:

Input:
input_text: "Tell me the 17th Fibonacci number."
chosen_tool_info: \{
    "name": "code interpreter",
    "summary": "Run the code through code_interpreter and return a dictionary including a log of the code run and whether it was successful or not.",
    ...
\}
tool_input: \{
    "code": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n-1):\n        a, b = b, a + b\n    return a\n\nprint(fibonacci(17))"
\}
tool_result: \{
    "result": "987\n",
    "success": true
\}

Output:
"The 17th Fibonacci number is 987."
"""

RESPONSE_GENERATE_HINT = """
You should only output the string of response, such as "The 17th Fibonacci number is 987.". Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
"""