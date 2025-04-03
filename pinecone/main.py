import asyncio
from embedding import PineconeUploader
import os
async def main():
    uploader = PineconeUploader(api_key= os.getenv("PINECONE_API_KEY"), index_name="physic_Testing")
    physics_directory = "dataset/physics"
    await uploader.create_vectorstore(physics_directory)

if __name__ == "__main__":
    asyncio.run(main())