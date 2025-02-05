from fastapi import FastAPI
from ScholiumModel.model import compile_graph 
from ScholiumModel.citation_handler import get_citation
# For Debugging Purposes
import logging
logger = logging.getLogger('uvicorn.error')

graph = compile_graph()
app = FastAPI()


'''
"""
FastAPI server for the Scholium question-answering system.

This module provides a REST API interface to interact with the Scholium model,
which uses a graph-based architecture to retrieve and generate answers from a knowledge base.

Endpoints:
    GET /requests/{query}:
        Processes a natural language query and returns relevant information from the knowledge base.
        
        Args:
            query (str): The user's question or query text
            
        Returns:
            response (str): The response from the model

Example:
    GET /requests/"What papers discuss machine learning?"
"""

'''
@app.get("/requests/{query}")
async def read_item(query: str):
    logger.debug(f"response: {query}")
    return graph.invoke({"messages": [{"role": "user", "content":query}]})['messages'][-1]

@app.get("/cite/{query}")
async def cite_iteam(query:str):
    get_citation(query=query)