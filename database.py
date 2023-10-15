import pinecone
import os
from dotenv import load_dotenv


load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENVIRONMENT')


index_name = 'problems-codebank'

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

index = pinecone.GRPCIndex(index_name)


def add_data(data: list) -> None:
    index.upsert(data)


def delete_data(data_ids: list) -> None:
    index.delete(ids=data_ids)


def update_data(data_id: str, new_value: list) -> None:
    index.update(data_id, values=new_value)


def make_db_query(embedding: list, filter_ids: list):
    return index.query(vector=embedding,
                       filter={
                           'id': {"$in": filter_ids},
                       },
                       top_k=len(filter_ids))


async def download_embeddings():
    pass
