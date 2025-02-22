'''
My own wrapper for a Pinecone index because the Langchain one only works for documents
'''

class ScholiumPineconeVectorStore():
    """
    A wrapper class for Pinecone vector database operations.
    
    This class provides an interface for embedding queries and performing similarity searches
    using a Pinecone vector index. It is designed to work with OpenAI embeddings.

    Attributes:
        client: The embedding client (typically OpenAIEmbeddings) used to generate embeddings
        index: The Pinecone index instance to perform vector searches against

    Args:
        embedding_client: An embedding client that provides embedding generation functionality
        index: A Pinecone index instance for vector storage and retrieval
    """
    def __init__(self, embedding_client, index) -> None:
        self.client = embedding_client
        self.index = index

    def _openAI_embed_query(self,query):
        return self.client.embeddings.create(
            input= query,
            model= "text-embedding-3-small"
        ).data[0].embedding
    
    def _filter_results(self, responses:list, score_cutoff = 0.8):
        '''
        This exists because, for some stupid reason, pinecone doesn't have a builtin way to cutoff low similarity responses
        '''
        return([
            response for response in responses if response['score'] >= score_cutoff
        ])
    
    def similarity_search(self, query, top_k = 10):
        embedded_query = self._openAI_embed_query(query)
        return self.index.query(
            namespace="",
            vector=embedded_query,
            top_k = top_k,
            include_metadata = True
        )['matches']
    
    def similarity_search_with_score_cutoff(self, query, top_k, score_cutoff):
        return self._filter_results(self.similarity_search(query, top_k), score_cutoff)
