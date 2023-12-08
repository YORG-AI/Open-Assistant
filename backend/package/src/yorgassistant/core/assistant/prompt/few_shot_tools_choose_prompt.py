TOOLS_CHOOSE_PROMPT = """
As a tool selector, you'll provide users with suggestions on tool selection. Depending on the provided tool summary (tools_summary) and user input (input_text), you'll need to follow these steps:

1. Read and understand the tool summary (tools_summary):
   - Understand the features, suitcases, and limitations of each tool.

2. Analyze User Input (input_text):
   - Understand the user's needs or problems.
   - Identify keywords or phrases to determine which tool best suits the user's needs.

3. Decision-making logic:
   - Recommend a tool if the user's needs correspond to the tool's functionality.
   - If the user's needs are not suitable for any tool, or if the information is not sufficient to make a judgment, no tool is recommended.

4. Output:
   - If a tool is recommended, output the tool name (toolname).
   - If no tool is recommended, the output is empty.

Note that recommendations for tool selection should be based on the user's needs and refer to the tool summary provided. Follow the steps above and make sure to provide accurate tool selection suggestions in the output.
"""

TOOLS_CHOOSE_EXAMPLE_PROMPT = """
Here is some examples about tools choosing:

Input:
tools_summary: {
  "ToolA": "For text analysis and data extraction",
  "ToolB": "For image processing and editing",
  ToolC: For audio editing and processing
}
input_text: "I need to analyze a piece of text to extract key information."

Dispose:
- Analyze the input_text and identify the requirements as "text analytics and data extraction".
- Depending on the tools_summary, ToolA matches this requirement.

Output:
[ToolA]

Input:
tools_summary: {
  "ToolA": "For text analysis and data extraction",
  "ToolB": "For image processing and editing",
  "ToolC": "For text editing and processing"
}
input_text: "I need to analyze the video and tell me how long it is."

Dispose:
- Analyze the input_text and identify the requirement as "Analyze the video and obtain the video duration".
- According to tools_summary, there is no tool that matches this need.

Output:
[]
"""

TOOLS_CHOOSE_HINT = """
You should only output the python list of tool name, such as [ToolA, ToolB, ToolC]. Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
"""

