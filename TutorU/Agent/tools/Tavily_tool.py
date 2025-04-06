import json
from tavily import TavilyClient
from typing import List, Dict
import os 
import dotenv
dotenv.load_dotenv()



class Tavily_tool:
    def __init__(self, api_key: str):
        self.tavily_client = TavilyClient(api_key=api_key)

        self.get_urls = self.get_urls
        
    def get_urls(self, query: str) -> Dict:
        """
        Fetches relevant URLs based on a query using the Tavily API.

        Args:
            query (str): The query text to fetch results for.

        Returns:
            Dict: A JSON-like dictionary with the search results (titles and URLs).
        """
        # Call the Tavily API's search method
        data = self.tavily_client.search(query)
        
        # Structure the data into a more readable JSON format
        results = {
            "query": query,
            "results": [
                {
                    "title": result['title'],
                    "url": result['url'],
                    "description": result.get('content', 'No description available')
                }
                for result in data['results']
            ],
            "response_time": data.get('response_time', 'N/A')
        }
        
        # Convert the dictionary to a pretty-printed JSON formatted string
        json_results = json.dumps(results, indent=4, separators=(',', ': '))  # Custom separators for better readability
        return json_results


# Example usage
if __name__ == "__main__":
    tavily_tool = Tavily_tool(api_key=os.getenv("TAVILY"))
    query = "What is physics?"
    urls = tavily_tool.get_urls(query)
    
    # Pretty print the JSON directly in the terminal
    print(urls)
