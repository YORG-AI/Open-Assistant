
## introduce
We provide a web dome that implements the functionality of the open source version of gpts through the use of yorgassistant, where users can define their own assistants and then turn on threads for conversations.

## setup
- Installation of dependencies
```shell
pip install -r requirements.txt
```
- Run the page
```shell
streamlit run streamlitdome.py
```
- Open the page.

On local port 8501：http://127.0.0.1:8501

You should enter the openai api key first, then you can experience this web dome

## Partial display
- Creating an Assistant
<div align="center">
    <img src="https://github.com/YORG-AI/Open-Assistant/assets/42194301/a8934f12-a076-47e6-9fe5-0b3efc21788b" width="500">
</div>


- use assistant tool
<div align="center">
    <img src="https://github.com/YORG-AI/Open-Assistant/assets/42194301/e964f81f-5daa-45fc-ac82-1cc9c73253eb" width="500">
</div>

## tools
We currently have a built-in swe_tool and code_interpreter, swe is a stateful tool and code is a function tool that you can add according to the yorgassistant documentation.

### todo
- data analysis tool 

It's a stateful TOOL that can help us do better data analysis

- understand codebase tool

It's a stateful TOOL that can help assistant understand code