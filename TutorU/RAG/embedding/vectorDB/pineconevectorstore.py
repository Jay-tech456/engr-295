import os
from pinecone import Pinecone, ServerlessSpec
from langchain.docstore.document import Document
import numpy as np
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
import time 


class PineconeVectorStore:
    def __init__(self, index_name, embedding, pinecone_api_key):
        
        self.pc = Pinecone(api_key=pinecone_api_key)
        

        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]

        # Check to see if the index already exist, if it does, it will connect it. 
        # By default, it will create an index
        if index_name not in existing_indexes:
            self.pc.create_index(
                name=index_name,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            while not self.pc.describe_index(index_name).status["ready"]:
                time.sleep(1)

        
        # Access the Pinecone index
        self.index = self.pc.Index(index_name)
        print("Vector Store Successfully connected")

    

    def similarity_search_by_vector(self, embedding, k=2):
        """Perform similarity search in Pinecone."""
        # Perform similarity search with the given embedding
        results = self.index.query(
            vector=embedding,
            top_k=k,
            include_values=False,
            include_metadata=True,
        )
        
        
        if results.get("matches"):
            return [
                Document(
                    page_content=f"Sub-topic: {result['metadata'].get('sub_topic', 'N/A')}\n"
                                f"Text: {result['metadata'].get('text', 'N/A')}\n"
                                f"Role: {result['metadata'].get('role_1', 'N/A')}\n"
                                f"Source: {result['metadata'].get('source', 'N/A')}", 
                    metadata=result['metadata']
                )
                for result in results['matches']
            ]
        else:
            print("No matches found")
            return []


    def as_retriever(self):
        """Return the vector store as a retriever."""
        return self
