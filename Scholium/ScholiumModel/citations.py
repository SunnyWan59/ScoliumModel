"""
This module provides utilities for formatting academic citations in varying styles.

The module contains functions to handle different aspects of citation formatting:
- Converting dates to proper Chicago format
- Formatting author lists with proper punctuation
- Converting metadata dictionaries into complete Chicago-style citations

Functions:
    format_date(date_str: str) -> str:
        Converts YYYY-MM-DD dates to 'Month Day, Year' format
        Example: "2023-01-15" -> "January 15, 2023"
        
    format_authors(authors_str: str) -> str: 
        Formats comma-separated author lists with proper Chicago style
        Example: "Smith, John, Jones, Mary" -> "John Smith and Mary Jones"
        
    format_author_name_mla(name: str, invert: bool = False) -> str:
        Formats a single author name in MLA style
        Example: "Smith, John" -> "John Smith" (invert=False) or "Smith, John" (invert=True)
        
    format_authors_mla(authors_str: str) -> str:
        Formats multiple author names in MLA style with proper rules for 1, 2 or 3+ authors
        
    format_date_mla(date_str: str) -> str:
        Converts YYYY-MM-DD dates to MLA format "D Mon. YYYY"
        Example: "2023-01-15" -> "15 Jan. 2023"
        
    metadata_to_chicago(metadata: dict) -> str:
        Converts a metadata dictionary into a complete Chicago citation
        Example: "Author. 'Title.' arXiv, Month Day, Year. URL."
        
    metadata_to_mla(metadata: dict) -> str:
        Converts a metadata dictionary into a complete MLA citation
        Example: "Last, First, et al. 'Title.' arXiv, D Mon. YYYY, URL."

Example:
    metadata = {
        'Authors': 'Smith, John, Jones, Mary',
        'Title': 'Machine Learning Advances',
        'Published': '2023-01-15'
    }
    
    citation = metadata_to_chicago(metadata)
    # Returns: "Smith, John, and Mary Jones. 'Machine Learning Advances.' January 15, 2023."


"""

import datetime

# ---------------------------
# Chicago-Style Functions
# ---------------------------
def format_date(date_str):
    """
    Convert a date string in YYYY-MM-DD format to 'Month Day, Year'.
    If the date string is invalid or empty, return the original string.
    """
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return date_str

def format_authors(authors_str):
    """
    Convert a comma-separated authors string into a properly formatted list:
    'Author1, Author2, and Author3'
    """
    # Split the string on commas and strip whitespace
    authors_list = [author.strip() for author in authors_str.split(',')]
    if len(authors_list) > 1:
        # Join all but the last with commas, then add ', and' before the final author
        return ', '.join(authors_list[:-1]) + ", and " + authors_list[-1]
    else:
        return authors_str

def metadata_to_chicago(metadata):
    """
    Convert the metadata dictionary into a Chicago-style citation.
    
    For an arXiv preprint, this outputs a citation like:
    
        Author1, Author2, and Author3. "Title." arXiv, Month Day, Year. URL.
    """
    # Extract and format the authors
    authors_raw = metadata.get('Authors', 'Unknown author')
    authors = format_authors(authors_raw)
    
    # Extract the title and ensure it's in quotes
    title = metadata.get('Title', 'Untitled')
    
    # Choose a publication date:
    # Prefer the 'Published' date, but if not available, fall back to 'published_first_time'
    published = metadata.get('Published')
    if not published or published.lower() == 'none':
        published = metadata.get('published_first_time', '')
    published_date = format_date(published) if published else "n.d."  # n.d. = no date
    
    # Get the URL from the entry_id field
    url = metadata.get('entry_id', '')
    
    # If the URL indicates an arXiv paper, include that label in the citation.
    source_label = "arXiv" if "arxiv" in url.lower() else ""
    
    # Assemble the citation
    if source_label:
        citation = f"{authors}. \"{title}.\" {source_label}, {published_date}. {url}."
    else:
        citation = f"{authors}. \"{title}.\" {published_date}. {url}."
    
    return citation

# ---------------------------
# APA-Style Functions
# ---------------------------
def format_author_name_apa(name):
    """
    Convert a name from "First Middle Last" to "Last, F. M.".
    """
    parts = name.strip().split()
    if not parts:
        return ""
    last = parts[-1]
    initials = [p[0] + '.' for p in parts[:-1]]
    return f"{last}, {' '.join(initials)}" if initials else last

def format_authors_apa(authors_str):
    """
    Format a comma-separated authors string for APA style.
    For multiple authors, APA uses an ampersand before the final name.
    Example: "Last, F. M., Last, F. M., & Last, F. M."
    """
    authors_list = [author.strip() for author in authors_str.split(',') if author.strip()]
    formatted_authors = [format_author_name_apa(author) for author in authors_list]
    
    if not formatted_authors:
        return "Unknown author"
    elif len(formatted_authors) == 1:
        return formatted_authors[0]
    else:
        return ', '.join(formatted_authors[:-1]) + ", & " + formatted_authors[-1]

def format_date_apa(date_str):
    """
    Convert a date string in YYYY-MM-DD format to APA style: "YYYY, Month DD"
    """
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y, %B %d")
    except (ValueError, TypeError):
        return date_str

def metadata_to_apa(metadata):
    """
    Convert metadata into an APA-style citation.
    Example:
      Last, F. M., Last, F. M., & Last, F. M. (YYYY, Month DD). Title [Preprint]. arXiv. URL
    """
    authors_raw = metadata.get('Authors', 'Unknown author')
    authors = format_authors_apa(authors_raw)
    
    title = metadata.get('Title', 'Untitled')
    
    published = metadata.get('Published') or metadata.get('published_first_time', '')
    date_str = format_date_apa(published) if published and published.lower() != 'none' else "n.d."
    
    url = metadata.get('entry_id', '')
    
    # Note: For an arXiv preprint, APA style suggests indicating [Preprint] and the source.
    citation = f"{authors} ({date_str}). {title} [Preprint]. arXiv. {url}"
    return citation

# ---------------------------
# MLA-Style Functions
# ---------------------------
def format_author_name_mla(name, invert=True):
    """
    For MLA, if invert=True, convert "First Last" to "Last, First".
    Otherwise, return the name unchanged.
    """
    parts = name.strip().split()
    if not parts:
        return ""
    if invert:
        if len(parts) == 1:
            return parts[0]
        else:
            last = parts[-1]
            first_names = " ".join(parts[:-1])
            return f"{last}, {first_names}"
    else:
        return name.strip()

def format_authors_mla(authors_str):
    """
    Format the authors for MLA style.
    MLA rules:
      - For three or more authors, list only the first author (inverted) followed by "et al."
      - For two authors, list the first inverted and the second in normal order.
      - For one author, simply invert the name.
    """
    authors_list = [author.strip() for author in authors_str.split(',') if author.strip()]
    if not authors_list:
        return "Unknown author"
    
    if len(authors_list) >= 3:
        return f"{format_author_name_mla(authors_list[0], invert=True)}, et al."
    elif len(authors_list) == 2:
        return f"{format_author_name_mla(authors_list[0], invert=True)} and {authors_list[1]}"
    else:
        return format_author_name_mla(authors_list[0], invert=True)

def format_date_mla(date_str):
    """
    Convert a date string in YYYY-MM-DD format to MLA style: "D Mon. YYYY"
    Example: "2023-01-10" becomes "10 Jan. 2023"
    """
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        month_abbr = {
            1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.",
            5: "May", 6: "June", 7: "July", 8: "Aug.",
            9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Dec."
        }
        day = dt.day
        month = month_abbr[dt.month]
        year = dt.year
        return f"{day} {month} {year}"
    except (ValueError, TypeError):
        return date_str

def metadata_to_mla(metadata):
    """
    Convert metadata into an MLA-style citation.
    Example:
      Last, First, et al. "Title." arXiv, D Mon. YYYY, URL.
    """
    authors_raw = metadata.get('Authors', 'Unknown author')
    authors = format_authors_mla(authors_raw)
    
    title = metadata.get('Title', 'Untitled')
    
    published = metadata.get('Published') or metadata.get('published_first_time', '')
    date_str = format_date_mla(published) if published and published.lower() != 'none' else ""
    
    url = metadata.get('entry_id', '')
    
    citation = f"{authors}. \"{title}.\" arXiv, {date_str}, {url}."
    return citation


if __name__ == '__main__':
    md = {'Authors': 'Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou', 'Published': '2023-01-10', 'Summary': 'We explore how generating a chain of thought -- a series of intermediate\nreasoning steps -- significantly improves the ability of large language models\nto perform complex reasoning. In particular, we show how such reasoning\nabilities emerge naturally in sufficiently large language models via a simple\nmethod called chain of thought prompting, where a few chain of thought\ndemonstrations are provided as exemplars in prompting. Experiments on three\nlarge language models show that chain of thought prompting improves performance\non a range of arithmetic, commonsense, and symbolic reasoning tasks. The\nempirical gains can be striking. For instance, prompting a 540B-parameter\nlanguage model with just eight chain of thought exemplars achieves state of the\nart accuracy on the GSM8K benchmark of math word problems, surpassing even\nfinetuned GPT-3 with a verifier.', 'Title': 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models', 'categories': ['cs.CL', 'cs.AI'], 'comment': 'None', 'doi': 'None', 'entry_id': 'http://arxiv.org/abs/2201.11903v6', 'journal_ref': 'None', 'links': ['http://arxiv.org/abs/2201.11903v6', 'http://arxiv.org/pdf/2201.11903v6'], 'primary_category': 'cs.CL', 'published_first_time': '2022-01-28', 'start_index': 0.0}

    print(metadata_to_chicago(md))