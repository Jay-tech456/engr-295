from tools.Discord_tool import Discord_tool
from tools.Retrive_tool import Retrive_tool

from tools.Tavily_tool import Tavily_tool
from langchain.embeddings import OllamaEmbeddings
from dotenv import load_dotenv
import os
import json
load_dotenv()



class Tools():
    def __init__(self, embeddings):
        pinecone_api_key = os.getenv('PINECONE_API_KEY')
        index_name = os.getenv('INDEX_NAME')
        discord_webhook_url = os.getenv('DISCORD_WEBHOOK')
        tavily_api_key = os.getenv('TAVILY')
        # sms_key = os.getenv('sms_key')
        # admin_email = os.getenv('sender_email')
        # admin_password = os.getenv('sender_password')
        
        # Create instances
        discord_instance = Discord_tool(discord_webhook_url)

        retrieve_instance = Retrive_tool(index_name, embeddings, pinecone_api_key)

        tavily_instance = Tavily_tool(tavily_api_key)
        
        # Binding the tools and the services with the tool itself
        discord_tool = discord_instance.send
        retrieve_tool = retrieve_instance.as_retriever
        tavily_tool = tavily_instance.get_urls
        

        self.tools = [discord_tool, retrieve_tool, tavily_tool]
        
     
    def toolkits(self):
        return self.tools
    

if __name__ == "__main__": 
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    test = Tools(embeddings)
    li = test.toolkits()
    
    Tavily = li[2]
    response_json = Tavily("What is physics?")
    

    response_data = json.loads(response_json)
    urls = "\n".join([f"Title: {item['title']}\nURL: {item['url']}" for item in response_data['results']])
    

    Discord_tool = li[0]
    discord_response = Discord_tool(urls)
    

    print("Search Results for 'What is physics?':\n", urls)
    print("Discord Response:", discord_response)