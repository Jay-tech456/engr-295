import sys 
import os
from typing import Dict
from langchain.embeddings import OllamaEmbeddings


sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from vectorDB.pineconevectorstore import PineconeVectorStore


class Retrive_tool: 
    def __init__(self, index_name, embeddings, pinecone_api_key): 
        self.index_name = index_name
        self.embeddings = embeddings
        self.pinecone_api_key = pinecone_api_key

        self.Pc = PineconeVectorStore(self.index_name, self.embeddings, self.pinecone_api_key)
        print("Pinecone successfully connected")

        self.as_retriever = self.retrieve

    def retrieve(self, query: str) -> list:
        """
        Retrieves Physics documents using cosine similarity search from Pinecone vector database.

        Args:
            query (str): Search query for physics datasets 

        Returns:
            list: Matching top 5 documents  documents from Pinecone database
        """
        retrieved_docs = self.Pc.similarity_search_by_vector(query)
        return retrieved_docs

# if __name__ == "__main__":
#     embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     Retrive_tool = Retrive_tool("physics", embeddings, "pcsk_4JbxFQ_ER3PXrERZ8MZCFnuCVVvSSyMvwwbY12TNjS9v3mvhArhqRBKSL3ybBVRxyRFUge")
#     li = Retrive_tool.retrieve("Quantumn Theory")
