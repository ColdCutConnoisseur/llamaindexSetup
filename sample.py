"""Example setup for llamaindex / openAI index and query"""

import os

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader


def index_documents(reference_folder_path, index_save_file):
    """Alternative would be to setup the 'Google Drive' data connector.
       But this will take a bit more setup in allowing access to your
       drive folder vs. using a collab notebook (setting up google dev project).
    """
    print("Reading and loading documents in folder...")
    reference_documents = SimpleDirectoryReader(reference_folder_path).load_data()
    print("Documents loaded!")

    # Construct the index from documents
    print("Constructing index...")
    tbg_index = GPTSimpleVectorIndex(reference_documents)
    print("Index constructed!")

    # Save the index
    print("Saving index...")
    tbg_index.save_to_disk(index_save_file)
    print("Index saved!")

    return tbg_index

def load_index(reference_folder_path, index_save_file):
    tbg_index = None

    # If file exists...
    if os.path.isfile(index_save_file):
        tbg_index = GPTSimpleVectorIndex.load_from_disk(index_save_file)

    # Otherwise create the initial index
    else:
        tbg_index = index_documents(reference_folder_path, index_save_file)

    return tbg_index


def execute_query_and_return_response(reference_folder_path, index_save_file, query_text):
    tbg_index = load_index(reference_folder_path, index_save_file)

    print("Index created / loaded successfully!")

    query_response = tbg_index.query(query_text)

    return query_response



if __name__ == "__main__":
    import config_file as cf


    os.environ['OPENAI_API_KEY'] = cf.AKEY

    REFERENCE_FOLDER_PATH = cf.PATH_TO_FOLDER_TO_INDEX # This is the path to your drive reference folder
    INDEX_SAVE_FILE = "TBG_index.json"

    EXAMPLE_QUERY = "Which is the largest Egyptian pyramid?"

    sample_response = execute_query_and_return_response(REFERENCE_FOLDER_PATH, INDEX_SAVE_FILE, EXAMPLE_QUERY)

    print(sample_response)
