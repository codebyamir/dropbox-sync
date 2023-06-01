# Syncs entire folder structure from Dropbox to local directory 

import dropbox
import logging
import sys
import argparse
from util import sync
from dropbox.exceptions import AuthError

# Configure logging to std out with timestamps
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',)

# Reduce logging noise by not logging INFO statements from the Dropbox SDK 
logging.getLogger('dropbox').setLevel(logging.WARNING)

TOKEN_FILE='token_dropbox.txt'
access_token = ''

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-s", "--source", help="Dropbox source folder")
    argParser.add_argument("-d", "--destination", help="Local destination folder")

    # parse arguments
    args = argParser.parse_args(args=None if sys.argv[1:] else ['--help'])

    try:
        # Read Dropbox access token from file
        access_token = open(TOKEN_FILE).read()
    except FileNotFoundError as err:
        logging.error(err)
        sys.exit('A file named ' + TOKEN_FILE + ' containing the Dropbox access token must exist in this directory.')

    # Authenticate with Dropbox
    with dropbox.Dropbox(access_token) as dbx:
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
