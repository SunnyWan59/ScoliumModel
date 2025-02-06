import os
from dotenv import load_dotenv
import time

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

from ScholiumModel.citations import metadata_to_chicago, metadata_to_apa, metadata_to_mla


load_dotenv()

citation_styles = {
    "chicago": metadata_to_chicago,
    "mla" : metadata_to_mla,
    "apa" : metadata_to_mla
}

DB_URI = os.environ.get("DB_URI")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

def get_citation(query:str, citation_style):
    if citation_style in citation_styles:
        make_citation = citation_styles[citation_style]
    else:
        raise SyntaxError("This citation style does not exist or has not been implemented yet")
    citations = []
    retrieved_docs = vector_store.similarity_search(query.strip("\""), k=10)
    for doc in retrieved_docs:
        citations.append(make_citation(doc.metadata))
    return "\n\n".join(citations)


if __name__ == "__main__":
    start_time = time.time()
    # print(get_citation("We explore how generating a chain of thought—a series of intermediate reasoning steps—significantly improves the ability of large language models to perform complex reasoning", "chicago"))
    print(get_citation(" For rationale-augmented training and finetuning methods, it is costly to create a large set of high quality rationales, which is much more complicated than simple input–output pairs used in normal machine learning." ,"chicago"))
    # print(get_citation("Consider one’s own thought process when solving a complicated reasoning task such as a multi-step math word problem", "chicago"))
    print("--- %s seconds ---" % (time.time() - start_time))
