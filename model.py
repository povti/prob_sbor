from sentence_transformers import SentenceTransformer
from utils import make_input
from database import add_data, delete_data, update_data, make_db_query

embedder = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')


def create_embedding(title: str, statement: str) -> list:
    return embedder.encode(make_input(title, statement)).tolist()


def add_problem(title: str, statement: str, problem_id) -> None:
    add_data([(str(problem_id), create_embedding(title, statement), {'id': problem_id})])


def delete_problem(problem_id) -> None:
    delete_data([str(problem_id)])


def update_problem(problem_id, new_title: str, new_statement: str) -> None:
    update_data(str(problem_id), create_embedding(new_title, new_statement))


def search(title: str, statement: str, ids: list) -> list:
    query_embedding = create_embedding(title, statement)
    results = make_db_query(query_embedding, list(map(str, ids)))
    sorted_ids = []
    for item in results['matches']:
        sorted_ids.append(item['id'])
    return sorted_ids
