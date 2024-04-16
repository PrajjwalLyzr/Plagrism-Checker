import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()

# Setup your config
st.set_page_config(
    page_title="Plagrism Checker",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Plagrism Checker by Lyzr")
st.markdown("### Welcome to the Plagrism Checker!")
st.markdown("Plagrism Checker app offers you checking the originality of content with the help of GenAI !!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Plagrism Checker

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 

open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def Plagrism_Checker(original_content, plagrised_content):
    
    content_strategy_analyst = Agent(
        prompt_persona="""You are a Content Strategy Analyst expert who can easily detect plagrism in the content provided by user.""",
        role="Content Strategy Analyst", 
    )

    plagrism_checker =  Task(
        name="Content Generator",
        agent=content_strategy_analyst,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions=f"Use the description provided, Compare the provided text: {plagrised_content} with the original source material : {original_content} to ensure it has been sufficiently altered to avoid plagiarism.",
        log_output=True,
        enhance_prompt=False,
        default_input=original_content
    )


    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="Plagrism Checker",
        completion_message="App Generated all things!",
        tasks=[
            plagrism_checker,
        ],
    ).run()

    return main_output


if __name__ == "__main__":
    style_app() 
    original = st.text_area("Write the original content")
    plagrism = st.text_area('Provide plagrised content')

    button=st.button('Submit')
    if (button==True):
        generated_output = Plagrism_Checker(original_content=original,plagrised_content=plagrism)
        title_output = generated_output[0]['task_output']
        st.write(title_output)
        st.markdown('---')
   
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Automata Agent suggest the 10 unique content topics that would differentiate your brand. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)