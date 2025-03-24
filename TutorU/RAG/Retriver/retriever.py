import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from vectorDB.pineconevectorstore import PineconeVectorStore
from langchain_community.embeddings import OllamaEmbeddings

class Retriever:
    def __init__(self, index_name, embeddings, pinecone_api_key):
        self.index_name = index_name
        self.embeddings_url = embeddings
        self.pinecone_api_key = pinecone_api_key

        # Setting up all the instances to help us retrive the Kth Nearest Neighbors
        self.embeddings = self.setup_embeddings()
        self.vectorstore = self.load_vectorstore()
        self.retriever = self.create_retriever()

    def setup_embeddings(self):
        return OllamaEmbeddings(model="nomic-embed-text")

    def load_vectorstore(self):
        print("Established Pinecone Connection")
        return PineconeVectorStore(index_name=self.index_name, embedding=self.embeddings, pinecone_api_key=self.pinecone_api_key)

    def create_retriever(self):
        print("Creating retriever")
        return self.vectorstore.as_retriever()
    
# if __name__ == "__main__": 
#     test = Retriever("physics-smaller", OllamaEmbeddings(model="nomic-embed-text"), "pcsk_4JbxFQ_ER3PXrERZ8MZCFnuCVVvSSyMvwwbY12TNjS9v3mvhArhqRBKSL3ybBVRxyRFUge")
#     vector_store = test.create_retriever()
#     embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     query = "What is quantum Mechanics?"
#     query_embedding = embeddings.embed_query(query)
    
#     results = vector_store.similarity_search_by_vector(query_embedding)
#     print(results)