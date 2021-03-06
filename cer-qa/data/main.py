import pandas as pd
import time
import os
import multiprocessing as mp
from multiprocessing import freeze_support
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from file_preparation import download_file, rotate_pdf, pickle_pdf_xml
from pdf_metadata import get_pdf_metadata


if __name__ == '__main__':

    # Necesary to avoid the error with multiprocessing
    # For more info (Windows): https://www.kite.com/python/docs/exceptions.RuntimeError
    # If using Linux/MacOS: https://pythonspeed.com/articles/python-multiprocessing/
    freeze_support()

    # Update the path when adding a new list of projects
    index_path = os.path.join(os.getcwd(), 'data/raw/index_for_projects/index_of_pdfs_for_major_projects_with_esas.csv')

    # Load the list of projects
    index = pd.read_csv(index_path)

    # Download files
    count = download_file(os.getcwd(), index)
    print("{} Files were downloaded from {} URL links".format(count, len(index)))

    # Rotate files
    count = rotate_pdf(os.getcwd(), index)
    print("{} Files were successfully rotated".format(count))

    # Convert to pickle files
    for pdf_folder_name, pickle_file_folder_name in {('pdfs', 'pickled_pdfs'), ('rotated_pdfs', 'pickle_rotated_pdfs')}:
        pdf_folder_path = os.path.join(os.getcwd(), 'data\\raw', pdf_folder_name)
        pdf_file_paths = [os.path.join(pdf_folder_path, file)
                        for file in os.listdir(pdf_folder_path) if file.endswith('.pdf')]
        pickle_folder_path = os.path.join(os.getcwd(), 'data\\interim\\', pickle_file_folder_name)

        # multiprocessing
        args = [(file, pickle_folder_path) for file in pdf_file_paths]
        starttime = time.time()
        with mp.Pool(mp.cpu_count()) as pool:
            pool.starmap(pickle_pdf_xml, args)
        print("{} Files were successfully converted to pickle files in {} seconds".format(len(pdf_file_paths), time.time() - starttime))
        # time ends and delta displayed
        print('That took {} seconds'.format(time.time() - starttime))

    # Add metadata and export to csv
    index_with_metadata = get_pdf_metadata(os.getcwd(), index)
    metadata_file_path = os.path.join(os.getcwd(), 'data/interim/intermediate_index_files/index_with_metadata.csv')
    index_with_metadata.to_csv(metadata_file_path, index=False, encoding='utf-8-sig')