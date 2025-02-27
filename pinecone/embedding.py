import json
import os
from pathlib import Path
from tqdm import tqdm
from pinecone import Pinecone
import numpy as np
import pickle
from langchain_community.embeddings import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PINECONE_API_KEY")

class PineconeUploader:
    def __init__(self, api_key, index_name, dimension=768):
        if not API_KEY:
            raise ValueError("API Key is missing. Make sure it's set in the .env file.")
        
        self.api_key = API_KEY
        self.index_name = index_name
        self.dimension = dimension
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Initialize Pinecone with new syntax
        self.pc = Pinecone(api_key=self.api_key)
        
        # Check if index exists, if not create it
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric='cosine'
            )
        
        self.index = self.pc.Index(self.index_name)

    def load_and_process_documents(self, directory_path):
        documents = []
        physics_dir = Path(directory_path)
        
        if not physics_dir.exists():
            raise ValueError(f"Directory not found: {directory_path}")

        for json_file in tqdm(list(physics_dir.glob("*.json")), desc="Loading files"):
            tqdm.write(f"Loading file: {json_file}")
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Process the physics problem-solution pair
                metadata = {
                    "role_1": data.get("role_1", "unknown"),
                    "topic": data.get("topic;", "unknown"),
                    "sub_topic": data.get("sub_topic", "unknown"),
                    "source": str(json_file.name)
                }
                
                # Combine problem and solution for embedding
                content = f"Problem: {data.get('message_1', '')}\nSolution: {data.get('message_2', '')}"
                documents.append({"metadata": metadata, "content": content})
                
        return documents

    async def create_vectorstore(self, physics_dir):
        documents = self.load_and_process_documents(physics_dir)
        tqdm.write("Uploading vectors to Pinecone")

        # Checkpointing setup
        checkpoint_file = Path("physics_checkpoint.pkl")
        start_idx = 0
        if checkpoint_file.exists():
            with open(checkpoint_file, "rb") as f:
                start_idx = pickle.load(f)
            tqdm.write(f"Resuming from checkpoint: {start_idx}")

        batch_size = 50
        for i in tqdm(range(start_idx, len(documents), batch_size), desc="Upserting vectors", unit="batch"):
            batch_docs = documents[i:i + batch_size]
            batch_vectors = []

            for idx, doc in enumerate(batch_docs):
                try:
                    # Generate embedding using OllamaEmbeddings
                    embedding = self.embeddings.embed_query(doc["content"])
                    # Generate a unique vector ID
                    vector_id = f"{doc['metadata']['topic']}_{doc['metadata']['sub_topic']}_{i+idx}"
                    
                    vector = {
                        "id": vector_id,
                        "values": embedding,
                        "metadata": {
                            **doc["metadata"],
                            "content": doc["content"]  # Store content in metadata for retrieval
                        }
                    }
                    batch_vectors.append(vector)
                except Exception as e:
                    tqdm.write(f"Error processing document {i+idx}: {str(e)}")
                    continue

            if batch_vectors:
                try:
                    # Upsert vectors to Pinecone
                    self.index.upsert(vectors=batch_vectors)
                except Exception as e:
                    tqdm.write(f"Error upserting batch: {str(e)}")
                    continue

            # Save checkpoint
            with open(checkpoint_file, "wb") as f:
                pickle.dump(i + batch_size, f)

        # Cleanup checkpoint file after completion
        if checkpoint_file.exists():
            checkpoint_file.unlink()

        tqdm.write("Vector upload completed.")
        return self.index