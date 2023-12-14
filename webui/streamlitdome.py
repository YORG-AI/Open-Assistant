import copy
import os
import streamlit as st
from streamlit.logger import get_logger
from datetime import datetime
import yorgassistant
class SessionState:
    def init_state(self):
        """Initialize session state variables."""
        st.session_state['assistant'] = []
        st.session_state['user'] = []

        st.session_state['selected_page_common'] = False
        st.session_state['selected_create_assistant'] = False
        st.session_state['selected_history'] = None
        st.session_state['thread_obj'] = None

    def clear_state(self):
        """Clear the existing session state."""
        st.session_state['assistant'] = []
        st.session_state['user'] = []
        st.session_state['selected_page_common'] = False
        st.session_state['selected_create_assistant'] = False
        st.session_state['selected_history'] = None
        st.session_state['thread_obj'] = None

class StreamlitUI:

    def __init__(self, session_state: SessionState):
        self.init_streamlit()
        self.session_state = session_state

    def init_streamlit(self):
        """Initialize Streamlit's UI settings."""
        st.set_page_config(
            # layout='wide',
            page_title='yorgassistant-web',
            page_icon='yorg.png')
        # Add Viewit logo image to the center of page
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("yorg.png", width=200)
        st.header(':robot_face: :blue[Open-assistants] Web Demo ', divider='rainbow')
        with open('README.md', 'r') as readme_file:
            readme_content = readme_file.read()
        st.markdown(readme_content, unsafe_allow_html=True)
        st.sidebar.title('setup')

    def setup_sidebar(self):
        yorgassistant.Threads.set_threads_yaml_path('data/threads.yaml')
        yorgassistant.Assistants.set_assistants_yaml_path('data/assistants.yaml')
        yorgassistant.Tools.set_tools_yaml_path('tools.yaml')
        
        
        with st.sidebar:
            st.subheader("gobal setup", divider='gray')
            proxy_agree = st.checkbox('set proxy',value=False)
            if proxy_agree:
                proxy =  st.number_input(label = "Proxy port",value=10809)
            else:
                proxy = 0
            api_key = st.text_input('openai api key(required):','', type="password")
            if not api_key:
                st.warning("please provide OpenAI API key.")
                
            # 设置代理
            if proxy_agree:
                os.environ['http_proxy'] = f'http://127.0.0.1:{proxy}'
                os.environ['https_proxy'] = f'http://127.0.0.1:{proxy}'
            os.environ['OPENAI_CHAT_API_KEY'] = api_key

            st.subheader("chatbox setup", divider='gray')
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button('create assistant'):
                    st.session_state['selected_create_assistant'] = True
                    st.session_state['selected_page_common'] = False
                    st.session_state['selected_history'] =None
                    
            assistants_list = yorgassistant.Assistants.get_all_assistants()
            assistants_list = list(reversed(assistants_list))
            if len(assistants_list)==0:
                st.warning("please create assistant.")
            else:
                choose_assistant = st.selectbox("choose assistant:", [assistant.name for assistant in assistants_list]) 
                for assistant in assistants_list:
                    if choose_assistant == assistant.name:
                        assistant_id = assistant.id
                st.session_state['page_common_assistant_id'] = assistant_id
                if len(choose_assistant)==0:
                    st.warning("please create assistant.")
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    if st.button('New   Chat  Box'):
                        st.session_state['selected_create_assistant'] = False
                        st.session_state['selected_page_common'] = True
                        st.session_state['selected_history'] =None
                        st.session_state['thread_obj'] = yorgassistant.Threads.create()
                st.subheader("chat history", divider='gray')
                history_nums = st.slider(label="history nums:", min_value=1, max_value=20,step=1,value=5)
                col1, col2, col3 = st.columns([1,4,1])
                with col2:
                    threads_list = yorgassistant.Threads.get_all_threads()
                    threads_list = list(reversed(threads_list))
                    history_nums = min(len(threads_list), history_nums)
                    last_threads = threads_list[:history_nums]
                    for i, thread in enumerate(last_threads):
                        btn_name = datetime.fromtimestamp(thread.created_at).strftime('%Y-%m-%d %H:%M:%S')
                        if st.button(btn_name, key=f"button_{i}"):
                            st.session_state['selected_history'] = thread.id
                            st.session_state['selected_create_assistant'] = False
                            st.session_state['selected_page_common'] = False
            st.write('---')
            st.caption("© Made by yorg 2023. All rights reserved.")
            st.caption('''By using this chatbot, you agree that the chatbot is provided on 
                    an "as is" basis and that we do not assume any liability for any 
                    errors, omissions or other issues that may arise from your use of 
                    the chatbot.''')
        
        
        if st.session_state['selected_history']:
            st.session_state['thread_obj'] = yorgassistant.Threads.from_id(st.session_state['selected_history'])
            st.session_state['page_common_assistant_id'] = st.session_state['thread_obj'].config.assistant_id if st.session_state['thread_obj'].config.assistant_id else assistant_id
            StreamlitPage().page_commen(st.session_state['page_common_assistant_id'])

        if st.session_state['selected_create_assistant'] and not st.session_state['selected_page_common']:
            StreamlitPage().create_assistants()
        elif st.session_state['selected_page_common'] and not st.session_state['selected_create_assistant']:
            st.session_state['assistant'] = []
            st.session_state['user'] = []
            StreamlitPage().page_commen(st.session_state['page_common_assistant_id'])



    def render_user(self, prompt: str):
        with st.chat_message('user'):
            st.markdown(prompt)

    def render_assistant(self, action):
        with st.chat_message('assistant'):
            self.render_action(action)


    def render_action(self, action):
        action_content = action['content']
        if action['type'] == 'success':
            if action_content['tool']=='':
                action_content['tool'] = 'No use tool'
            with st.expander(action_content['tool'], expanded=False):
                st.markdown(
                    "<p style='text-align: left;display:flex;'> <span style='font-size:14px;font-weight:600;width:170px;text-align-last: justify;'>tool</span><span style='width:14px;text-align:left;display:block;'>:</span><span style='flex:1;'>"  # noqa E501
                    + action_content['tool'] + '</span></p>',
                    unsafe_allow_html=True)
                st.markdown(
                    "<p style='text-align: left;display:flex;'> <span style='font-size:14px;font-weight:600;width:170px;text-align-last: justify;'>tool_type</span><span style='width:14px;text-align:left;display:block;'>:</span><span style='flex:1;'>"  # noqa E501
                    + action_content['tool_type'] + '</span></p>',
                    unsafe_allow_html=True)
                st.markdown(
                    "<p style='text-align: left;display:flex;'><span style='font-size:14px;font-weight:600;width:170px;text-align-last: justify;'>tool_response</span><span style='width:14px;text-align:left;display:block;'>:</span></p>",  # noqa E501
                    unsafe_allow_html=True)
                st.markdown(action_content['tool_response'])
            st.markdown(action['assistant']['message'])
        else:
            with st.expander(action['type'], expanded=False):
                st.markdown('error information:'+action_content['message'])
            st.markdown('chat error you must input correct openai api key')
                
class StreamlitPage:
    def page_commen(self,assistant_id:str):
        if st.session_state['thread_obj']  == None:
            thread = yorgassistant.Threads.create()
            st.session_state['thread_obj']  = thread
            st.session_state['assistant'] = []
            st.session_state['user'] = []
        else:
            st.session_state['assistant'] = []
            st.session_state['user'] = []
            for history in st.session_state['thread_obj'].config.message_history:
                st.session_state['user'].append(history[0]['user'])
                st.session_state['assistant'].append(history[1]['assistant'])
        assistants_list = yorgassistant.Assistants.get_all_assistants()
        name = ''
        for assistant in assistants_list:
            if assistant.id == assistant_id:
                name = assistant.name
        title = f'current assistant name : {name}'
        st.subheader(title)
        # TODO 添加历史信息
        for prompt, agent_return in zip(st.session_state['user'],
                                        st.session_state['assistant']):
            st.session_state['ui'].render_user(prompt)
            st.session_state['ui'].render_assistant(agent_return)

        if user_input := st.chat_input(''):
            st.session_state['ui'].render_user(user_input)
            st.session_state['user'].append(user_input)
            with st.spinner('Wait for it...'):
                if st.session_state['assistant']:
                    last_assistant_message = st.session_state['assistant'][-1]
                    if 'next_stages_info' in last_assistant_message['content']['tool_response']:
                        tool_response = last_assistant_message['content']['tool_response']
                        tool_response=eval(tool_response)
                        next_stages_info = tool_response['next_stages_info']
                        keys = list(next_stages_info.keys())
                        agent_return = st.session_state['thread_obj'].run(assistant_id,user_input,goto=keys[0])
                    else:
                        agent_return = st.session_state['thread_obj'].run(assistant_id,user_input)
                else:
                    agent_return = st.session_state['thread_obj'].run(assistant_id,user_input)
            print(f'agent_return:{agent_return}')
            st.session_state['assistant'].append(copy.deepcopy(agent_return))
            st.session_state['ui'].render_assistant(agent_return)
    def create_assistants(self):
        st.subheader('create assistant setting')
        name=st.text_input('assistant name:','')
        model=st.selectbox("model name:", ["gpt-4-1106-preview","gpt-4"])
        instructions=st.text_area('assistant instructions :','')
        tools_options = st.multiselect('sselect assistant tools:',['swe_tool','code_interpreter'])
        tools=[{'type':tool} for tool in tools_options]
        if st.button('Submit'):
            assistant = yorgassistant.Assistants.create(name=name, model=model, instructions=instructions, tools=tools)
            st.session_state['selected_create_assistant'] = False
            st.session_state['selected_page_common'] = True
            st.session_state['page_common_assistant_id'] = assistant.id


def main():
    logger = get_logger(__name__)
    # Initialize Streamlit UI and setup sidebar
    if 'ui' not in st.session_state:
        session_state = SessionState()
        session_state.init_state()
        st.session_state['ui'] = StreamlitUI(session_state)
    else:
        st.set_page_config(
            # layout='wide',
            page_title='yorgassistant-web',
            page_icon='yorg.png')
        st.header(':robot_face: :blue[Open-assistants] Web Demo ', divider='rainbow')
    st.session_state['ui'].setup_sidebar()

    

if __name__ == '__main__':
    main()