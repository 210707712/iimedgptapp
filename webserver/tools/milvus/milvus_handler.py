from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, MilvusClient
from tools.milvus.config import Config


class MilvusManager:
    def __init__(self):
        self.conn = connections.connect(host=Config.MILVUS_HOST, port=Config.MILVUS_PORT, db_name="zhjkproject")
        # self.client = MilvusClient(uri=f"http://localhost:19530", db_name="zhjkproject")
        self.client = MilvusClient(uri=f"http://{Config.MILVUS_HOST}:{Config.MILVUS_PORT}", db_name="zhjkproject")

    def create_collection(self, knowledge_id):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=Config.DIMENSION),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048)
        ]
        schema = CollectionSchema(fields, "Document Embeddings")
        collection = Collection(f"knowledge_{knowledge_id}", schema)
        return collection

    def create_index(self, knowledge_id):
        collection = Collection(f"knowledge_{knowledge_id}")
        if collection.has_index():
            return
        else:
            index = {"index_type": "IVF_FLAT", "params": {"nlist": 10}, "metric_type": "COSINE"}
            collection.create_index("embedding", index)

    def insert_embeddings(self, knowledge_id, embeddings, texts, filename):
        collection = Collection(f"knowledge_{knowledge_id}")
        data = [
            embeddings.tolist(),
            texts,
            filename
        ]
        print(data)
        collection.insert(data)

    def search_query(self, knowledge_id, query_embedding):
        collection = Collection(f"knowledge_{knowledge_id}")
        search_params = {"metric_type": "COSINE", "params": {}}
        collection.load()
        results = collection.search([query_embedding],
                                    anns_field="embedding",
                                    param=search_params,
                                    limit=5,
                                    output_fields=["id","text", "title"])
        return results

    def has_collection(self, knowledge_id):
        if self.client.has_collection(f"knowledge_{knowledge_id}"):
            return True
        return False
