# dropbox-sync
Syncs folders from Dropbox to local machine

# Setup steps

## Install packages
```
pip install -r requirements.txt
```

## Get Dropbox API access token 

1. Go to: https://dropbox.com/developers/apps
2. Register your own App - e.g., call it "personal access to research data"
3. Copy secret *access token* after registering your app (click on Get Token)
4. Paste that access token to a file called *token_dropbox.txt*. 

# Usage

```
python dropbox_backup.py --source "/Shared/My Files" --destination "/backups/"
```

