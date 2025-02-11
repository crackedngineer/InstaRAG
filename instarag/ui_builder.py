import streamlit as st

class UIBuilder(object):
    def __init__(self, config: dict):
        self.config = config

    def __introduction(self):
        """ 
        Set main content title and description
        """
        st.title(self.config["meta"]["title"])
        if "description" in self.config:
            st.caption(self.config["description"])
    
    def __chat_interface(self):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}
            ]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Generate response only if a model is selected and user has entered a prompt
            # if model:
            #     with st.chat_message("assistant"):
            #         with st.spinner("Thinking..."):

            #             # Generate assistant response
            #             msg = model.chat(st.session_state.messages[1:])
            #             if msg:
            #                 st.write(msg)
            #                 st.session_state.messages.append(
            #                     {"role": "assistant", "content": msg}
            #                 )
            # else:
            #     st.info("Please select a model to continue or check the API key")

    def execute(self):
        self.__introduction()
        self.__chat_interface()