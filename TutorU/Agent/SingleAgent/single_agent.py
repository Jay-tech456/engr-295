

import time
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import sys 
import os
from langchain_mistralai import ChatMistralAI

# Having a system path so that the files are all readable
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from tools.toolbox import Tools
from utils.utils import AgentState


class PhysicsAgent:
    def __init__(self):
        self.mistral_model = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key="ERbtRhtyGei4jY4AXn4QkrWSfGzlpLbP")

        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        Tool = Tools(embeddings)
        self.tools = Tool.tools

        self.model_with_tool = self.mistral_model.bind_tools(self.tools)

        self.system_prompt = self.create_system_prompt()

    def create_system_prompt(self):
        return SystemMessage(
            content="""
                You are an AI physics assistant, strictly designed to help students understand physics concepts.  
                You also have access to specific tools to assist with study-related activities.  

                ### **Rules and Constraints:**  
                1. **Physics-Only Responses:**  
                - You will **only answer physics-related questions**.  
                - Topics include: classical mechanics, electromagnetism, quantum mechanics, thermodynamics, relativity, astrophysics, particle physics, and other core physics subjects.  
                - If a query is not physics-related, you will respond with:  
                    **"I can only answer physics-related questions."**  

                2. **Clarifications Only for Physics:**  
                - If a question is unclear, ask for clarification **only if it appears to be physics-related**.  

                3. **Tool Usage Instructions:**  
                - You have access to the following tools:  

                - **Retrieve Tool:**  
                    - Fetch textbook content or reference materials.  
                    - Search by topic or concept to find detailed explanations.  
                    - If the requested information is not found, explain this to the student.  

                - **Discord Tool:**  
                    - Use this tool to assist with study-related activities on Discord.  
                    - Capabilities:  
                        - **Generate Study Guides:** Create detailed, organized study guides based on requested topics.  
                        - **Create Study Group Plans:** Outline study group objectives, schedules, and topics.  
                        - **Schedule Study Sessions:** Suggest dates/times for group or individual study sessions.  
                    - Ensure that all Discord messages are clear, structured, and professional. 

                - **Tavily Tool:**  
                    - Use this tool to gather and provide relevant search results based on user queries.  
                    - Capabilities:  
                        - **Search for Information:** Retrieve search results that are highly relevant to the user's query from trusted sources.  
                        - **Provide URLs:** Extract the URLs from the search results and ensure they link directly to the relevant articles or resources.  
                        - **Return Summaries:** In addition to URLs, provide concise summaries for the retrieved articles to give users a quick preview of the content.  
                    - Ensure that all search results are relevant, concise, and properly formatted. Provide URLs with a clear title and ensure that summaries (if provided) are brief yet informative.  
                    - Maintain professionalism and accuracy in your responses, ensuring that the information shared is reliable and up-to-date.
                    

                4. **History Awareness:**  
                - Use the conversation history to maintain context.  
                - If history is insufficient, rely on the retrieve tool.  

                5. **Formatting and Clarity:**  
                - Present information clearly and concisely.  
                - Use bullet points, equations, or step-by-step reasoning when necessary.

                ---
                **Conversation History:**  
                {history}  

                **Context:**  
                {context}  

                **Question:**  
                {question}
        
        """
        )

    def agent(self, state: AgentState, config: RunnableConfig):
        time.sleep(1)
        response = self.model_with_tool.invoke(
            [self.system_prompt] + state["messages"], config=config)
        return {"messages": [response]}


# GPT Composed Main
if __name__ == "__main__":
    agent = PhysicsAgent()
    state: AgentState = {"messages": []}
    config = RunnableConfig()

    print("🧠 PhysicsAgent is ready! Type your physics questions below.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting PhysicsAgent. See you next time!")
            break

        # Add user message to the state
        state["messages"].append(HumanMessage(content=user_input))

        # Invoke the agent
        result = agent.agent(state, config)

        # Add AI response to the message history
        ai_response = result["messages"][0]
        state["messages"].append(ai_response)

        # Print response
        print(f"Agent: {ai_response.content}\n")