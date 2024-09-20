from elasticsearch import Elasticsearch
from typing import List, Dict, Optional

# Elasticsearch 클라이언트 초기화
es = Elasticsearch(
    [{'scheme': 'http', 'host': '13.209.81.191', 'port': 9200}]
)

def search_books(query: Optional[str] = None) -> List[Dict]:
    if query:
        try:
            # Elasticsearch 검색 쿼리 (vector_field 제외)
            response = es.search(
                index="booklist",
                body={
                    "_source": ["id", "isbn13", "bookname", "authors", "publisher", "publication_year", "bookimageurl", "description"],  # 필드 제한
                    "query": {
                        "match": {
                            "bookname": query  # 책 제목으로 검색
                        }
                    }
                }
            )
            # 검색 결과 추출
            hits = response['hits']['hits']
            return [{"id": hit["_id"], **hit["_source"]} for hit in hits]
        except Exception as e:
            print(f"Error searching in Elasticsearch: {e}")
            return []
    return []
