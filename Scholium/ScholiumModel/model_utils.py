import re

def extract_paper_titles(text):
    """
    Finds all substrings in `text` that are enclosed in matching single or double quotes.
    
    Parameters:
        text (str): The input string.
    
    Returns:
        List[str]: A list of quoted substrings, including the surrounding quote characters.
    """
    pattern = r'(["\'])(.*?)\1'
    matches = re.finditer(pattern, text)
    return [match.group(0) for match in matches]


def get_paper_metadata(titles:list[str], metadata):
    metadata_list = []
    for title in titles:
        if title.strip("\"") in metadata:
            metadata_list.append(metadata[title.strip("\"")])
    return metadata_list

