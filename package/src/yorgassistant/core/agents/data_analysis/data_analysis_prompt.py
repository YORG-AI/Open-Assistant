from .planner_prompt import PLANNER_PROMPT

DA_PROMPT = """
You are a data scientist working on a project. You are working on a statistic modeling task.
"""


SINGLE_DF = """
You are working with a pandas dataframe in Python. The name of the dataframe is df.

The header rows of the dataframe are as follows:
{df_header}

"""


MULTIPLE_DF = """
You are working with {num_dfs} pandas dataframes in Python named df1, df2, etc. You

The header rows of the dataframe are as follows:
{df_headers}

"""

FILE_INFO = """system: Add a filename at {file_path}"""

FILE_INFOMATION_PROMPT = """
[File Name] {file_name}
[File Type] {file_type}
[File Path] {file_path}
"""


DATA_SCHEMA = """
The schema dictionary uses DataFrame column names as keys. For numeric columns, the value is another dictionary detailing its type, min, and max values; for string columns, the value is simply string; and for others, it's the datatype as a string.

{data_schema}

The sample of the data:

{data_sample}

"""

# end

CODE_INTERPRETER_PREFIX = """
You are an AI code interpreter.
Your goal is to help users do a variety of jobs by executing Python code.

You should comprehend the user's requirements carefully & to the letter.
Then write python code to solve the problem.
All of the files path will be listed in a list followed by (file info):
All of the files schema will be listed in a dict followed by (data schema):
The question is as below:

------

"""


CODE_INTERPRETER_SUFFIX = """

------

***Your code should output answer to STDOUT. (i.e. use python `print` function)***
You need to put the code you generated inside the [] and surround it with triple backticks.
The example output is as follows:

------
## code_result
```python
python code you generated as a string"""


# Planner prompt

SUPPORT_PROJECT_TYPE = [
    "Regression",
    "Classification",
    "ANOVA",
    "Clustering",
    "Time Series",
    "Association Rules",
    "NLP",
    "Recommender System",
    "Dimension Reduction",  # only choose from PCA and tsne
    "Survival Analysis",
    "Longitudinal Analysis",
    "Causal Inference",
    "Non-Parametric",
    "Basic t-test",
    "Basic Chi-Square test",
    "Linear Regression",
    "Logistic Regression",
    "Time Series ARIMA",
    "Time Series SARIMA",
    "One-Way ANOVA",
    "Two-Way ANOVA",
    "Other",
]

PROJECT_TYPE_SELECTOR_PROMPT = """Here is my project requirement: {project_requirement}

Please tell me what type of project it is, and only output the project type.

If the type is other, please output "other: xxx" where xxx is the type.

You can choose from the following options: """ + ", ".join(
    SUPPORT_PROJECT_TYPE
)


REVISE_PLAN_PROMPT = """Here is my project context: {project_requirement}

We are at step {step_number}. Here is the previous step report result: {previous_result}

Now please revise the plan of following steps. Here is the plan:

{step_plans}

If no need to revise, please output "no need to revise" only.

"""


# Step filler prompt

STEP_FILLER_BODY_STEP1 = """Here is my project context:

{project_requirement}

Here is my project data (in a list):

(file info):

{file_info}

The data schema will be a dictionary that use file path as keys. For each file path key, the value is
another dictionary detailing its column names, data types, and other information.
Here is the data schema (in a dictionary):

{data_schema}

You should write code base on the provided data schema and file info. Now we start step 1. Here is the step 1 plan:

{step_plan}

"""

STEP_FILLER_BODY_STEP_NOT1 = """Here is my project context: {project_requirement}

Here is my project data (in a list):

{file_info}

The data schema will be a dictionary that use file path as keys. For each file path key, the value is
another dictionary detailing its column names, data types, and other information.
Here is the data schema (in a dictionary):

{data_schema}

Here is the previous code for step {step_number_p}:

{step_code}

Here is the step {step_number_p} result:

{step_result}

You should write code base on the provided data schema and file info, and previous code, result. Now we start step {step_number}. Here is the step {step_number} plan:

{step_plan}

"""

STEP_FILLER_BODY_STEP_CONCLUSION = """Here is my project context: {project_requirement}

Here is the previous step report result: {previous_report}

Now we start step Conclusion. Here is the plan:

{step_plan}

You need to provide the report of the conclusion part. Please give suggestions of the previous steps report if needed.

"""


STEP_PARAGRAPH_PROMPT = """Here is my project context: {project_requirement}

Here is the step {step_number} plan:

{step_plan}

Here is the step {step_number} code:

{step_code}

Here is the step {step_number} result:

{step_result}

Now please convert the result into this part of the report.
You need to carefully analysis the result and organize it into a report with markdown syntax accorading to the step plan.
include table, plot, and text if neccessary.
The plot indicated in result with [plot i] will be inserted in the report with [plot i] only. This [] does not apply to tables.
Don't include any markdown when indicating the plot. Only use [plot i] to indicate the location.
If there is no [plot i] in the result, please do not include any plot in the report.

"""  # TODO, need to craft the prompt of result generating!!!!


#####

SAMPLE_REQUIREMENT = """In this project we want to analysis the dataset containing information on 76 people who undertook one of three diets (referred to as diet A, B and C). The main question of the project is to determine which diet was best for losing weight. It is important because the analysis result can help the company select the best product to invest. In this project we will use the one factor ANOVA method to carry out the conclusion, and obtain the pairwise confidence interval for all three diets.
"""

# SAMPLE_REQUIREMENT = """Use the ”basic controls” and Lin’s estimator ˆτI to estimate the causal effect on fall grades (grade_20059_fall) with three independent separate treatments ssp, sfsp, sfp. Use robust standard error. “Basic controls” report estimates of the coefficient on assignment-group dummies in models that control for sex (female), mother tongue (english), high school grade quartile (hsgroup), and number of courses as of November 1 (numcourses_nov1). The names inside () are names in the columns of the dataset
# """

SAMPLE_REVISE_REQUIREMENT = """Fix the following code and make it executable
"""

CODE_REVISE_PROMPT = """Here is my project data (in a list):

{file_info}

The data schema will be a dictionary that use file path as keys. For each file path key, the value is
another dictionary detailing its column names, data types, and other information.
Here is the data schema (in a dictionary):

{data_schema}

Here is my existing code:

{code}

Now I need you revise the code to make it executable. The information to fix it is as follows:
{requirement}. Please provide the all of the revised code, not only the modified part.
Please don't change the data loading path.

```python
python code you generated"""