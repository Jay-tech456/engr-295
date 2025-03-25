import asyncio
# from pinecone.embedding import PineconeUploader
from embedding import PineconeUploader

async def main():
    uploader = PineconeUploader(index_name="physics")
    physics_directory = "/Users/chenshuzhu/Desktop/engr-295/dataset/physics"
    await uploader.create_vectorstore(physics_directory)

if __name__ == "__main__":
    asyncio.run(main())