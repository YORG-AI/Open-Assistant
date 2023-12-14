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
{
    "thoughts": {
        "text": "用户需要分析一段文字并提取关键信息。",
        "reasoning": "根据工具概要，ToolA专用于文本分析和数据提取，这与用户的需求相符。",
        "criticism": "虽然用户的需求明确，但仍需考虑文本的具体类型和分析的深度来确保ToolA能够满足需求。",
        "speak": "您希望提取的关键信息是什么类型的？这有助于更好地使用ToolA。"
    },
    "tool": {
        "name": ["ToolA"]
    }
}


Input:
tools_summary: {
  "ToolA": "For text analysis and data extraction",
  "ToolB": "For image processing and editing",
  "ToolC": "For text editing and processing"
}
input_text: "I need to analyze the video and tell me how long it is."

Output:
{
    "thoughts": {
        "text": "用户需要分析视频并了解视频时长。",
        "reasoning": "用户的需求是与视频分析相关的，而提供的工具中没有直接针对视频处理或分析的工具。ToolA和ToolC主要用于文本处理，ToolB则用于图像处理和编辑。",
        "criticism": "虽然ToolB与图像处理有关，但它并不适用于视频分析或处理视频时长这类需求。此外，没有工具被描述为直接支持视频处理功能。",
        "speak": "看来我们目前提供的工具都不适合您的需求，因为它们主要是用于文本和图像处理，而不是视频分析。"
    },
    "tool": {
        "name": [
            
        ]
    }
}

Input:
tools_summary: {
"ToolA": "For text analysis and data extraction",
"ToolB": "For image processing and editing",
"ToolC": "For creating interactive web applications"
}
input_text: "I need to analyze survey data and create an interactive web dashboard to display the results."

Output:
{
    "thoughts": {
        "text": "用户需要分析调查数据并创建一个交互式的网络仪表板来展示结果。",
        "reasoning": "根据工具摘要，ToolA 适用于文本分析和数据提取，而 ToolC 适用于创建交互式的网络应用程序。",
        "criticism": "虽然 ToolA 适用于数据分析，但无法创建网络仪表板；ToolC 可以创建交互式的网络应用，但可能不具备分析数据的功能。",
        "speak": "根据您的需求，ToolA 和 ToolC 都可能是有用的工具，但需要结合使用才能满足您的需求。"
    },
    "tool": {
        "name": ["ToolA", "ToolC"]
    }
}



"""

TOOLS_CHOOSE_HINT = """
You should only respond in JSON format as described below 
Response Format: 

{{{{
    "thoughts": {{{{
        "text": "your thoughts in the current context",
        "reasoning": "reasoning for tool selection and input content",
        "criticism": "critical thinking on tool selection and input in current context",
        "speak": "words you want to speak to the user",
    }}}},
    "tool": {{{{
        "name": ['tool_name'], 
    }}}}
}}}}

The strings corresponding to "text", "reasoning", "criticism", and "speak" in JSON should be described in Chinese.

If you don't need to use a tool(like solely chat scene), or have already reasoned the final answer associated with user input from the tool, You must abide by the following rules: 
1. The tool's name in json is [].

Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
Ensure the output can be parsed by Python json.loads.
Don't output in markdown format, something like ```json or ```,just output in the corresponding string format

"""

