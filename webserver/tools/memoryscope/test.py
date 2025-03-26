import unittest

from memoryscope.core.models.llama_index_embedding_model import LlamaIndexEmbeddingModel
from memoryscope.core.storage.llama_index_es_memory_store import LlamaIndexEsMemoryStore
from memoryscope.scheme.memory_node import MemoryNode

def setUp(self):
    config = {
        "module_name": "dashscope_embedding",
        "model_name": "text-embedding-v2",
        "clazz": "models.llama_index_embedding_model",
    }
    emb = LlamaIndexEmbeddingModel(**config)

    config = {
        "index_name": "0708_2",
        "es_url": "http://localhost:9200",
        "embedding_model": emb,
        "use_hybrid": True

    }
    self.es_store = LlamaIndexEsMemoryStore(**config)
    self.data = [
        MemoryNode(
            content="The lives of two mob hitmen, a boxer, a gangster and his wife, "
                    "and a pair of diner bandits intertwine in four tales of violence and redemption.",
            memory_type="observation",
            user_name="0",
            status="valid",
            memory_id="aaa123",

        )]



def save_memory(self, userid: str, query: str):

    for node in self.data:
        self.es_store.insert(node)
     
    node = MemoryNode(
        content=query,
        memory_type="profile",
        user_name=userid,
        memory_id="ggg567",
        meta_data={"5": "5"}
    ) 
    self.es_store.insert(node)
    
def update_memory(self, userid: str, query: str):
    self.es_store.update(MemoryNode(
            content=query,
            memory_type="profile",
            user_name=userid,
            memory_id="ggg567"
        ))
    
def load_memory(self, userid: str, query: str):
    filter_dict = {
       "user_name": userid, 
    }
    res = self.es_store.retrieve_memories(query=query, filter_dict=filter_dict, top_k=15)
    return res

def load_memory_asyncio(self, userid: str, query: str):
    import asyncio
    filter_dict = {
       "user_name": userid, 
    }
    res = asyncio.run(self.es_store.a_retrieve_memories(query=query, filter_dict=filter_dict, top_k=15))
    return res

def detele_memory(self, userid: str, query: str):
    self.es_store.delete(MemoryNode(
            content=query,
            memory_type="profile",
            user_name=userid,
            memory_id="ggg567"
        ))
    

def tearDown(self):
    self.es_store.close()