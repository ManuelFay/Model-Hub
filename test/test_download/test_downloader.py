import unittest
import os
import shutil

from model_hub import download
from model_hub.utils import get_torch_home


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.url = "https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"
        self.download_path = None
        self.cache_test = os.path.join(get_torch_home(), "model_hub_test")
        self.tearDown()

    def test_download(self):
        download_path = download(self.url, is_zip=False, cache_path=self.cache_test)
        self.download_path = download_path
        self.assertTrue(os.path.exists(self.download_path))

    def tearDown(self) -> None:
        if os.path.isdir(self.cache_test):
            shutil.rmtree(self.cache_test)
