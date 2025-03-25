from langgraph.graph import MessagesState
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import sys
import os
from langchain_ollama import OllamaEmbeddings

# Adjusting system path so that we can import Retriever and utils
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from Retriver.retriever import Retriever
from utils.utils import State


class PhysicsTutor:
    def __init__(self, retriever):
        """Initialize the tutor with retriever, LLM, and prompt template."""
        self.llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
        self.retriever = retriever
        self.prompts = self.setup_prompt()

    def setup_prompt(self):
        """Define the physics-specific system prompt."""
        template = """
        You are an AI physics assistant, strictly designed to help students understand physics concepts.

        ### **Rules and Constraints:**  
        1. **Physics-Only Responses:**  
           - You will **only answer physics-related questions**.  
           - Topics include: classical mechanics, electromagnetism, quantum mechanics, thermodynamics, relativity, astrophysics, particle physics, and other core physics subjects.  

        2. **Strict Rejection of Non-Physics Queries:**  
           - Under no circumstances will you answer questions outside the scope of physics (e.g., history, literature, biology, general math, pop culture, etc.).  
           - If asked an unrelated question, respond with:  
             **"I can only answer physics-related questions."**  

        3. **Clarifications Only for Physics:**  
           - If a question is unclear, ask for clarification **only if it appears to be related to physics**.  

        4. **Physics-Specific Abilities:**  
           - You can **generate detailed explanations** with step-by-step reasoning.  
           - You can **create study guides** on specific physics topics.  
           - You can **build narrations** and illustrative examples to explain physics concepts.

        ---
        Here is the conversation history: {history}
        
        **Context:**  
        {context}

        **Question:**  
        {question}
        """
        return ChatPromptTemplate.from_template(template)

    def query(self, query):
        """Retrieve documents from the vector store based on the query."""
        query_embedding = self.retriever.embeddings.embed_query(query)
        docs = self.retriever.vectorstore.similarity_search_by_vector(
            embedding=query_embedding,
            k=5
        )
        return docs

    def format_docs(self, docs):
        """Format retrieved documents into a readable string."""
        return "\n\n".join([doc.page_content for doc in docs])

    def generate(self, state: MessagesState, config: RunnableConfig) -> dict:
        """Generate a response with conversation history."""
        user_input = state["messages"][-1].content if state["messages"] else ""


        chat_history = [
            AIMessage(content=msg.content) if isinstance(msg, AIMessage) else BaseMessage(content=msg.content, type="user")
            for msg in state["messages"]
        ]

        input_data = {
            "question": user_input,
            "history": chat_history
        }

  
        user_id = config["configurable"].get("thread_id")
        if not user_id:
            raise ValueError("User ID is missing in the configuration.")
        

        chain = (
            RunnableMap(
                {
                    "context": lambda x: self.query(x["question"]),
                    "history": lambda x: chat_history,
                    "question": RunnablePassthrough()
                }
            )
            | self.prompts
            | self.llm
            | StrOutputParser()
        )

  
        response = chain.invoke(input_data)


        return {"messages": chat_history + [AIMessage(content=response)]}
