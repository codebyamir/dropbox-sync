# dropbox-sync
Syncs entire folder structure from Dropbox to local machine

Currently only supports individual Dropbox accounts and not Business/Team accounts.

## Setup steps

### Install packages
```
pip install -r requirements.txt
```

### Get Dropbox API access token 

1. Go to https://dropbox.com/developers/apps
2. Click the Create App button
3. Select Scoped Access and Full Dropbox 
4. Enter app name (must be unique)
5. Click Create App
6. Under the Permissions tab, select the following permissions:
- files.metadata.read
- files.content.read
7. Under the Settings tab, click the **Generate Token** button

# Configuration

- Create an environment variable named `DBX_ACCESS_TOKEN` for the access token 

## Usage

```
python dropbox_backup.py --source "/Shared/My Dropbox" --destination "/backups/"
```

