from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import shelve

# from langchain_community.llms import HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace

from langchain import hub
from langchain.agents import AgentExecutor, load_tools
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    ReActJsonSingleInputOutputParser,
)
from langchain.tools.render import render_text_description
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

st.title("Streamlit Chatbot Interface")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#lanchain-hugginface
# llm = HuggingFaceEndpoint(repo_id="HuggingFaceH4/zephyr-7b-beta")
# llm = HuggingFaceEndpoint(repo_id = "mistralai/Mistral-7B-Instruct-v0.3")
llm = HuggingFaceEndpoint(repo_id="HuggingFaceH4/zephyr-7b-beta",max_new_tokens=512,temperature=0.7,huggingfacehub_api_token='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')

# chat_model = ChatHuggingFace(llm=llm)

# tools = load_tools(["serpapi"], llm=llm)

# # setup ReAct style prompt
# prompt = hub.pull("hwchase17/react-json")
# prompt = prompt.partial(
#     tools=render_text_description(tools),
#     tool_names=", ".join([t.name for t in tools]),
# )

# # define the agent
# chat_model_with_stop = chat_model.bind(stop=["\nObservation"])
# agent = (
#     {
#         "input": lambda x: x["input"],
#         "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
#     }
#     | prompt
#     | chat_model_with_stop
#     | ReActJsonSingleInputOutputParser()
# )

# # instantiate AgentExecutor
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])


# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages


# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        # st.markdown("Hello how are you?")

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        # for response in client.chat.completions.create(
        #     model=st.session_state["openai_model"],
        #     messages=st.session_state["messages"],
        #     stream=True,
        # ):
        #     full_response += response.choices[0].delta.content or ""
        # res = agent_executor.invoke({
        # # "input": st.session_state["messages"]  "You are an expert at analysing stocks. Go through the details of the stocks and come up with a analysis. Analysis should not be very long. Focus should be on profit and how much reliable is the stock.\n Details are \n"+file_details + "\n Output should be in json format.Format is:\n" + "{\"Stock Name\":\"<Name of the stock>\", \"Final Answer\":\"<Complete Analysis>\",\"Profit Percentage\":\"<Calculated Profit percentage>\"}\n End when you have final analysis of the stock."
        #   "input": prompt})
        res = llm.invoke(prompt)
        # with st.chat_message(name = "bot", avatar= "🤖"):
        #    st.write(res)
        message_placeholder.markdown(res + "|")
        message_placeholder.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)