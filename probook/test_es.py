from elasticsearch import Elasticsearch

# Elasticsearch 클라이언트 생성
es = Elasticsearch(
    [{'scheme': 'http', 'host': '52.79.186.105', 'port': 9200}]
)

index_name = 'booklist'

def search_document(query):
    response = es.search(index=index_name, body={
        "query": {
            "match": {
                "bookname": query
            }
        }
    })
    return response

def main():
    search_query = "Example Book"  # 검색할 책 제목을 입력하세요.
    response = search_document(search_query)
    
    print("Search Results:")
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Source: {hit['_source']}")

if __name__ == "__main__":
    main()
