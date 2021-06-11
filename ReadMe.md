# Model Hub 

A simple helper library to download, use and cache machine learning models available online.
Library closely inspired by UKP Lab's caching scripts, and the Hugging Face `from_pretrained` and developed for personal use.

This library is configured for torch models, but can download and cache other filetypes from online URLs.

Simplest usage is achieved by hardcoding a download server path (google storage bucket) and using 
this library as a simple download and cache interface for ML models.


### Setup

In a new virtual environment, run:

```bash
pip install -r dev_requirements.txt
```

### Usage

```python
from model_hub import download

url = "https://xxx.xxx"
model_path = download(url)
```

### Arguments

- cache_path: Custom path to save model directory
- download_server: Path to a public Google Storage repository, public drive link, server
            example: "https://storage.googleapis.com/organization/models/"

- model_name_or_path: Model name from a Google Storage bucket, or the downloadable URL of a model or file.
        is_zip
  
- is_zip: By default True, setting it to False enables to download arbitrary file types (images, audio)

Returns: Downloaded model directory path or file path (if not zip)