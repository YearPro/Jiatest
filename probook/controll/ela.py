from elasticsearch import Elasticsearch
from typing import List, Dict, Optional

# Elasticsearch 클라이언트 초기화
es = Elasticsearch(
    [{'scheme': 'http', 'host': '52.78.167.144', 'port': 9200}]
)

def search_books(query: Optional[str] = None) -> List[Dict]:
    if query:
        # Elasticsearch 검색 쿼리
        response = es.search(
            index="booklist",
            body={
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
    return []
