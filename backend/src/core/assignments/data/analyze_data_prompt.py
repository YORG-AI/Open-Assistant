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


GEN_CODE = """
You should try to answer each question posed of you in a single line of python code:
{queries}

The output format is as follows:
{output_format}
"""


GEN_ANSWER = """
"""


CODE_FORMAT = """
```python
### Answer
[
    "code to answer query 1",
    "code to answer query 2",
    ...
]
```
"""


OUTPUT_SCHEMA = {}
