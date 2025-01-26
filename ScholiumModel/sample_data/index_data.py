import os
import time
from ScholiumModel.indexer import Indexer 
'''
A simple script that indexes the pdf's in the sample_data folder
'''

def already_indexed(file_path):
    """Reads each line from a file and stores it as a list of strings."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines & strip whitespace
    return lines

def append_list_to_file(file_path, lines):
    """Appends a list of strings to a file, one per line."""
    with open(file_path, "a", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def index_pdfs():
    '''
    Indexes the pdf's in the sample_data folder

    Really janky way of doing this, but it works for now
    '''
    alr_index = already_indexed("loaded.txt")
    indexer = Indexer()
    for file in os.listdir("pdfs/"):
        if file.endswith(".pdf"):
            file_path = os.path.join("pdfs/", file)
            print(file_path)
            if file_path not in alr_index:
                print(f"Indexing {file_path}")
                indexer.index_document(file_path)
                append_list_to_file("loaded.txt", [file_path])
                time.sleep(10) # Sleep for 10 seconds to avoid rate limiting
            else:
                print(f"Skipping {file_path} as it is already indexed")


if __name__ == "__main__":
    index_pdfs()