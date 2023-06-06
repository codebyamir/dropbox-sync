# Syncs entire folder structure from Dropbox to local directory 

import dropbox
import logging
import sys
import argparse
import os
from util import sync
from dropbox.exceptions import AuthError

# Configure logging to std out with timestamps
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',)

# Reduce logging noise by not logging INFO statements from the Dropbox SDK 
logging.getLogger('dropbox').setLevel(logging.WARNING)

# Configuration
ACCESS_TOKEN = os.environ['DBX_ACCESS_TOKEN']

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-s", "--source", help="Dropbox source folder")
    argParser.add_argument("-d", "--destination", help="Local destination folder")

    # parse arguments
    args = argParser.parse_args(args=None if sys.argv[1:] else ['--help'])

    # Authenticate with Dropbox
    with dropbox.Dropbox(ACCESS_TOKEN) as dbx:
        # Check that access token is valid
        try:
            dbx.users_get_current_account()
        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")
        
        logging.info('Successful login to Dropbox with account name ' + dbx.users_get_current_account().name.display_name)

        # Set source directory on Dropbox
        source_dir = args.source

        # Set target download directory on your local computer
        download_dir = args.destination

        # download files
        sync(dbx, source_dir, download_dir)
