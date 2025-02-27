import asyncio
from embedding import PineconeUploader

async def main():
    uploader = PineconeUploader(index_name="physics")
    physics_directory = "dataset/physics"
    await uploader.create_vectorstore(physics_directory)

if __name__ == "__main__":
    asyncio.run(main())