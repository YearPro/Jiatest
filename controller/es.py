from elasticsearch import Elasticsearch
from typing import List, Dict, Optional
import html  # HTML 엔티티 디코딩을 위한 모듈
import math  # NaN 검사를 위한 모듈

# Elasticsearch 클라이언트 초기화
es = Elasticsearch(
    [{'scheme': 'http', 'host': 'two', 'port': 9200}]
)

def contains_nan(data: Dict) -> bool:
    """
    데이터 딕셔너리에서 NaN 값이 있는지 확인합니다.
    """
    for key, value in data.items():
        if value is None:
            return True
        if isinstance(value, float) and math.isnan(value):
            return True
        if isinstance(value, str) and value.strip().lower() == 'nan':
            return True
    return False

def search_books(query: Optional[str] = None) -> List[Dict]:
    if query:
        try:
            # Elasticsearch 검색 쿼리 (vector_field 제외)
            response = es.search(
                index="booklist",
                body={
                    "_source": ["id", "isbn13", "bookname", "authors", "publisher",
                                "publication_year", "bookimageurl", "description"],  # 필드 제한
                    "query": {
                        "match": {
                            "bookname": query  # 책 제목으로 검색
                        }
                    }
                }
            )
            # 검색 결과 추출 및 NaN 값 필터링
            hits = response['hits']['hits']
            results = []
            for hit in hits:
                source = hit['_source']
                # 데이터에 NaN이 포함되어 있으면 해당 문서를 제외
                if contains_nan(source):
                    continue  # 이 문서는 건너뜁니다.
                # description 필드가 있는 경우 HTML 엔티티 디코딩
                if 'description' in source and source['description']:
                    source['description'] = html.unescape(source['description'])
                results.append({"id": hit["_id"], **source})
            return results
        except Exception as e:
            print(f"Error searching in Elasticsearch: {e}")
            return []
    return []
