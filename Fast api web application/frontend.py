import streamlit as st
import requests
from pydantic import BaseModel
import os

# Defining our backend API URL where we have our tool hosted

BACKEND_URL = "http://192.168.140.53:6090/query"


class QueryRequest(BaseModel):
    user_input: str

def main():
    st.title("Database Query Tool")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Displaying the  chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.markdown(message["content1"])

    # Taking user input
    user_input1 = st.chat_input("Enter your input")


    if user_input1:
            
        st.chat_message("Human").markdown(user_input1)
        # Add user message to chat history
        st.session_state.messages.append({"role": "Human", "content": user_input1,"content1":""})
        request_data = {"user_input":user_input1}
        print("request_data",request_data)

            # Sending our POST request to backend
        response = requests.post(BACKEND_URL, json=request_data)
        print("response",response)

            # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            
            with st.chat_message("assistant"):
                st.markdown(result["sql_query"])
                st.markdown(result["answer"])
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result["sql_query"], "content1":result["answer"]})
                
        else:
            st.error("Failed to process request. Please try again later.")

    
if __name__ == "__main__":
    main()
