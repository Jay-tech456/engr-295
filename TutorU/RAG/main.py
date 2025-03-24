from Generate.generation import PhysicsTutor
from Retriver.retriever import Retriever
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState
from dotenv import load_dotenv
import os

load_dotenv()
import time

if __name__ == "__main__":


    # Setting up the Basic retriver, tutor, and RunableConfig to help with the proper chatbot interface itself
    retriever = Retriever(os.getenv("INDEX_NAME"), 
                                   OllamaEmbeddings(model="nomic-embed-text"), 
                                   os.getenv('PINECONE_API_KEY'))

    tutor = PhysicsTutor(retriever)
    config = RunnableConfig(configurable={"thread_id": "user123"})

    # Will be used to store the chat history itself
    messages = []  

    print("\n **MENTORMIND is running...** Type 'exit' to quit.\n")

    while True:
        user_query = input("Please enter a physics-related question (or type 'exit' to quit): ")


        if user_query.lower() == "exit":
            print("\nExiting the program. Goodbye!")
            break

        # Append the user's message to the history
        messages.append(HumanMessage(content=user_query))
        
        # Create the state with the message history.
        state = MessagesState(messages=messages)

        print("\n**Human:** " + user_query)

        try:
            # Stream the AI's response in real-time
            response = tutor.generate(state, config)

    
            last_ai_message = None

            for message in response["messages"]:
                if isinstance(message, AIMessage):
                    last_ai_message = message

            # Display only the last Mentorbot messages itself. 
            if last_ai_message:
                print("\n **MentorMind:**", end=" ", flush=True)
                for char in last_ai_message.content:
                    print(char, end="", flush=True)
                    time.sleep(0.01)  

                messages.append(last_ai_message)

            print("\n")

        except Exception as e:
            print(f"\n Error while generating response: {str(e)}")

    print("\n **End of Program**")
