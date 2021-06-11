# pylint: disable=logging-format-interpolation
import logging
import os
from zipfile import ZipFile
import shutil

from model_hub.utils import http_get, get_torch_home


def download(model_name_or_path: str,
             is_zip: bool = True,
             cache_path: str = None,
             download_server: str = None):
    loader = ModelLoader(cache_path=cache_path, download_server=download_server)
    return loader(model_name_or_path, is_zip=is_zip)


class ModelLoader:
    def __init__(self, cache_path: str = None, download_server: str = None):
        """
        :param cache_path: Custom path to save model directory
        :param download_server: Path to a public Google Storage repository, public drive link, server
            example: "https://storage.googleapis.com/organization/models/"
        """
        self.default_cache_path = cache_path
        if cache_path is None:
            torch_cache_home = get_torch_home()
            self.default_cache_path = os.path.join(torch_cache_home, "model_hub")
        self.url_length_limit: int = 250
        self.download_server = download_server

    def __call__(self, model_name_or_path: str, is_zip: bool = True) -> str:
        """
        :param model_name_or_path: Model name from a Google Storage bucket, or the downloadable URL of a model or file.
        Local paths also work but using them would render this library useless.
        :return: Downloaded model directory path
        """

        input_name = model_name_or_path

        if model_name_or_path:
            logging.info("Load pretrained model: {}".format(model_name_or_path))

            if "/" not in model_name_or_path and "\\" not in model_name_or_path and not os.path.isdir(
                    model_name_or_path) and self.download_server:
                logging.info("Did not find a '/' or '\\' in the name. Assume to download model from server.")
                model_name_or_path = self.download_server + model_name_or_path + ".zip"

            if model_name_or_path.startswith(("http://", "https://")):
                model_url = model_name_or_path
                folder_name = model_url.replace("https://", "").replace("http://", "").replace("/", "_")[
                    :self.url_length_limit]

                model_path = os.path.join(self.default_cache_path, folder_name)
                os.makedirs(model_path, exist_ok=True)

                if not os.listdir(model_path):
                    if model_url.endswith("/"):
                        model_url = model_url[:-1]
                    logging.info("Downloading model from {} and saving it at {}".format(model_url, model_path))
                    try:
                        if is_zip:
                            zip_save_path = os.path.join(model_path, "model.zip")
                            http_get(model_url, zip_save_path)
                            with ZipFile(zip_save_path, "r") as zip_:
                                zip_.extractall(model_path)
                        else:
                            http_get(model_url, os.path.join(model_path, folder_name))
                            input_name = folder_name

                    except Exception as exception:
                        shutil.rmtree(model_path)
                        raise exception
            else:
                model_path = model_name_or_path

            # Load from disk
            if model_path is not None:
                logging.info("Load model from folder: {}".format(model_path))

                if os.path.exists(os.path.join(model_path, "config.json")):  # If model files are at root level
                    return model_path
                return os.path.join(model_path, input_name)

        raise NameError
