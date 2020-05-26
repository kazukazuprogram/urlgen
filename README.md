# urlgen
Get download URL from cloud storage service URL.

## Installation
```
pip install urlgen
```

## Usage
```
urlgen <URL>
```

## Options
`--password <password>`  
  Specify password. (available only uploader.jp)  
  If not specified a prompt will be opened.  
<!--
`--download, -d`  
  Download file.  
`--external-downloader <Commandline>`  
  Specify downloader command and args.  
  By default, the URL is added at the end, but you can specify the URL location by inserting "{URL}" in the Commandline.  
`-o, --output <file>`  
  Specify output filename.  
  This is valid only when "--external-downloader" is not specified.  
-->

## Available sites
- MEGAUPLOAD
- UploadHaven
- Google Drive (bug not fixed)
- Zippyshare
- MediaFire
- uploader.jp  
