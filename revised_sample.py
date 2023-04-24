"""Example setup for llamaindex / openAI index and query"""

import os
import csv

import PyPDF2
from llama_index import (GPTSimpleVectorIndex,
                         SimpleDirectoryReader,
                         Document)

from llama_index.langchain_helpers.text_splitter import TokenTextSplitter

import config_file as cf



def load_index():
    """If an index exists at the index_save_file path, load.
    Otherwise create a new index"""
    tbg_index = None

    # If file exists...
    if os.path.isfile(cf.INDEX_SAVE_PATH):
        tbg_index = GPTSimpleVectorIndex.load_from_disk(cf.INDEX_SAVE_PATH)

    # Otherwise create the initial index
    else:
        tbg_index = GPTSimpleVectorIndex([])

    return tbg_index

def execute_query_and_return_response(query_text):
    tbg_index = load_index()

    print("Index created / loaded successfully!")

    query_response = tbg_index.query(query_text)

    return query_response

def DEPRadd_documents_to_existing_index(reference_folder_path, index_save_file):
    existing_or_new_index = load_index(reference_folder_path, index_save_file)

    document = SimpleDirectoryReader(reference_folder_path).load_data()[0]
    text_splitter = TokenTextSplitter(separator=" ", chunk_size=2048, chunk_overlap=20)
    text_chunks = text_splitter.split_text(document.get_text())
    doc_chunks = [Document(t) for t in text_chunks]

    print("Document text finished chunking")

    for chunk in doc_chunks:
        existing_or_new_index.insert(chunk)

    return existing_or_new_index

def save_index(li_index, index_save_file):
    print("Saving index...")
    li_index.save_to_disk(index_save_file)
    print("Index saved!")

def load_good_files_csv():
    """Load the CSV containing files that have successfully been added to index"""
    good_files = []

    try:
        with open(cf.GOOD_FILE_PATH, 'r') as good_in:
            csv_reader = csv.reader(good_in)

            for row in csv_reader:
                good_files.append(row[0])

    except FileNotFoundError:
        pass

    return good_files

def save_good_files_list(files_list):
    """Save csv of files that were successfully added to the index"""
    if len(files_list) > 0:
        files_list = [[f] for f in files_list]
        with open(cf.GOOD_FILE_PATH, 'w') as good_out:
            csv_writer = csv.writer(good_out)

            csv_writer.writerows(files_list)

def build_index_around_errors(reference_folder_path):
    """Workaround for PyPDF2 EOF errors"""
    good_files = load_good_files_csv()
    bad_files = []

    print(f"Files already in index: {good_files}")

    new_or_existing_index = load_index()

    sys_sep = '/'

    all_files_in_directory = [reference_folder_path + sys_sep + file_name
                              for file_name in os.listdir(reference_folder_path)]

    for d_file in all_files_in_directory:

        # If file has already been handled, ignore
        if d_file in good_files:
            continue

        # Otherwise handle
        else:

            print(f"Attempting to add file: {d_file}...")

            in_files = [d_file]

            try:
                reference_doc = SimpleDirectoryReader(reference_folder_path, input_files=in_files).load_data()

                for doc in reference_doc:
                    new_or_existing_index.insert(doc)

                good_files.append(d_file)

            except PyPDF2.errors.PdfReadError:
                print(f"EOF Error for file: {d_file}")
                bad_files.append(d_file)

    print("Finished working through files in directory!")

    print("Saving successfully handled files...")
    save_good_files_list(good_files)
    print("Files list saved!")

    print("Saving Index...")
    save_index(new_or_existing_index, cf.INDEX_SAVE_PATH)
    print("Index Successfully Saved!")

    print("These were all of the bad files with EoF errors:")
    print(bad_files)




if __name__ == "__main__":

    # Config variables are now set in 'config_file.py'
    os.environ['OPENAI_API_KEY'] = cf.AKEY
    REFERENCE_FOLDER_PATH = cf.PATH_TO_FOLDER_TO_INDEX
    INDEX_SAVE_FILE = cf.INDEX_SAVE_PATH

    build_index_around_errors(REFERENCE_FOLDER_PATH)

    EXAMPLE_QUERY = "What is the diet of slender toads?"

    sample_response = execute_query_and_return_response(EXAMPLE_QUERY)

    print(sample_response)
