import dropbox
import os
import logging
import sys
from dropbox import Dropbox
from dropbox.exceptions import ApiError

# Retrieves the folder ID given a path
def get_folder_id(dbx: Dropbox, folder: str):
    try:
        metadata = dbx.files_get_metadata(path=folder)
        return metadata.id
    except ApiError:
        sys.exit('ERROR - Source folder not found in Dropbox: ' + folder)

# Downloads files locally
def sync(dbx: Dropbox, source_dir: str, download_dir: str):
    dropbox_folder_id = get_folder_id(dbx, source_dir)
    assert(dropbox_folder_id.startswith('id:'))

    result = dbx.files_list_folder(dropbox_folder_id, recursive=True)
    
    # determine highest common directory
    assert(result.entries[0].id==dropbox_folder_id)
    common_dir = result.entries[0].path_lower
    
    file_list = []
    
    def process_entries(entries):
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                file_list.append(entry.path_lower)
    
    process_entries(result.entries)
    
    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)
    
        process_entries(result.entries)
        
         
    logging.info('Downloading ' + str(len(file_list)) + ' files...')

    for fn in file_list:
        logging.info(fn)
        path = remove_suffix(download_dir, '/') + remove_prefix(fn, common_dir)
        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)))
        except Exception:
            1+1
        dbx.files_download_to_file(path, fn)
    
 
def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def remove_suffix(text, suffix):
    return text[:-(text.endswith(suffix) and len(suffix))]