from api.openalex import WorksHandler, IDHandler
from api.text_splitter import extract_search_parameters
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

from api.common_utils import parse_authors, get_referenced_works, inverted_index_to_string

def process_results(results):
    '''
    Only extract the important information from the OpenAlex Response
    
    Args:
        results (list): List of work objects from OpenAlex API
        
    Returns:
        list: List of dictionaries containing processed information
    '''
    processed_results = []

    for result in results:
        abstract_inverted_index = result.get('abstract_inverted_index')
        abstract = inverted_index_to_string(abstract_inverted_index) if abstract_inverted_index else "No abstract available"
        
        # Add journal information if available
        journal_info = None
        if 'primary_location' in result and result['primary_location']:
            if 'source' in result['primary_location'] and result['primary_location']['source']:
                journal_info = result['primary_location']['source'].get('display_name', '')
       
        processed_item = {
            'title': result.get('title', ''),
            'abstract': abstract,
            "open_alex_id": result.get("id", "").split("/")[-1] if result.get("id") else "",
            'metadata':{
                        'publication_date': result.get('publication_date', ''),
                        'authors': parse_authors(result.get('authorships', [])),
                        'referenced_works': get_referenced_works(result.get('referenced_works', [])),
                        'related_works': get_referenced_works(result.get("related_works", [])),
                        'doi': result.get('doi', ''),
                        'journal': journal_info,
                        'biblio': result.get('biblio', ' '),
                        }
        }
        processed_results.append(processed_item)
    
    return processed_results

def search_parameters_to_search(query: str, client: OpenAI, idhandler: IDHandler, workshandler: WorksHandler):
    params = extract_search_parameters(query, client=client)
    filters= {}
    if params.authors:
        authors = [idhandler.get_author_id(author) for author in params.authors]
        filters["author.id"] = "|".join(authors)
        
    if params.topics:
        topics = [topic_id for topic in params.topics if (topic_id := idhandler.get_topic_id(topic))]
        print(topics)
        if topics:
            filters["topics.id"] = "|".join(topics)
    filters["language"] = params.language if params.language else "en"
    
    n_papers = params.n_papers if params.n_papers else 10
    
    results = workshandler.search(query=params.query,filters=filters, n_results= n_papers)
    return(process_results(results=results))

if __name__ == '__main__':
    idhandler = IDHandler("sunny@scholium.ai")
    wh = WorksHandler("sunny@scholium.ai")
    query = "Find 15 papers about transformer models by Vaswani and Hinton in English from U of T"
    results = search_parameters_to_search(client=client, query=query, idhandler=idhandler, workshandler=wh)
    print(f"Found {len(results)} results")
    
    import json
    with open('search_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Results exported to search_results.json")
