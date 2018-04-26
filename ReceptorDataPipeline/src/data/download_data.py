import os
import logging
import dotenv
import re
from azure.storage.blob import BlockBlobService


def main(project_dir):
    
    blob_storage_account = os.getenv("BLOB_STORAGE_ACCOUNT")
    blob_storage_key = os.getenv("BLOB_STORAGE_KEY")
    container_name = os.getenv("BLOB_STORAGE_CONTAINER")
    blob_folder_path = os.getenv("BLOB_STORAGE_CSV_FOLDER")

    raw_data_dir = os.path.join(project_dir, 'data', 'raw')

    download_from_blob(blob_storage_account, blob_storage_key, container_name, blob_folder_path, local_folder = raw_data_dir)


def download_from_blob(storage_account, storage_key, container_name, blob_folder_path, local_folder):
    """ 
    Downloads file from blob storage
    """
    logger = logging.getLogger(__name__)
    block_blob_service = BlockBlobService(account_name=storage_account, account_key=storage_key)
    blob_list = block_blob_service.list_blobs(container_name, blob_folder_path + '/', delimiter='/')
    for blob in blob_list:
        if re.search('\.csv', blob.name):
            #Build local file path
            local_file_path = os.path.join(local_folder, os.path.basename(blob.name))
            logger.info("Donwloading file %(blob_name)s into %(local_file_path)s'" % {"blob_name": blob.name, "local_file_path": local_file_path})
            block_blob_service.get_blob_to_path(container_name, blob.name, local_file_path)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.WARN, format=log_fmt)

    # Get project directory
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # Load dotenv
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)
    
    # Run
    main(project_dir)