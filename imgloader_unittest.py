# -*- coding: utf-8 -*-
"""Unit test for module imgloader (programming exercise)

This unit test is designed to test the following functions

 * test_download_by_url
 * test_read_in_file
 * test_download_by_text_file

Note: The concept of mocking can be used to simulate the behavior of I/O and
other external services without the need of an actual test environment.
In this unit test it is only used exemplary to test file reading performance.
It could however be further elaborated to test server request and response errors
as well as other I/O operations like the writing or deleting of a file.
The result would be a unit test, which is fully independent of external services,
making it very fast and highly robust.
"""

import unittest
import os, io
from imgloader import download_by_text_file, download_by_url_list, read_in_file
from unittest.mock import patch, mock_open

class ImgLoaderUnitTest(unittest.TestCase):

    URL_VALID_IMAGE_1 = 'https://upload.wikimedia.org/wikipedia/id/b/b9/Donald_duck_stor_121201c.jpg'
    URL_VALID_IMAGE_2 = 'https://upload.wikimedia.org/wikipedia/en/2/21/DaisyDuck.png'
    URL_INVALID_IMAGE = 'https://www.wikipedia.org/'
    URL_BROKEN_LINK   = 'https://upload.wikimedia.org/wikipedia/id/b/b9/Donald_duck_stor_XXXX.jpg'

    # download_by_url_list ###################################################
	
    def test_download_by_url_list_with_empty_list(self):
        url_list = []                                                        
        self.assertEqual(download_by_url_list(url_list), 0)

    def test_download_by_url_list_with_valid_image_urls(self):
        url_list = [self.URL_VALID_IMAGE_1, self.URL_VALID_IMAGE_2]
        self.assertEqual(download_by_url_list(url_list), 2)

    def test_download_by_url_list_with_broken_image_urls(self):
        url_list = [self.URL_BROKEN_LINK, self.URL_VALID_IMAGE_2]
        self.assertEqual(download_by_url_list(url_list), 1)
		
    def test_download_by_url_list_with_invalid_image_format(self):
        url_list = [self.URL_INVALID_IMAGE, self.URL_VALID_IMAGE_2]
        self.assertEqual(download_by_url_list(url_list), 1)

    # read_in_file ###########################################################
		
    def test_read_in_file_for_open(self):
        filename = "foo.bar"
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            read_in_file(filename)
            mock_file.assert_called_with(filename, "r")
			
    def test_read_in_file_with_valid_input_file(self):
        data = self.URL_VALID_IMAGE_1 + '\n' + self.URL_VALID_IMAGE_2
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True):
            self.assertEqual(read_in_file("foo.bar"), data.split())

    def test_read_in_file_with_invalid_input_file(self):
        self.assertEqual(read_in_file("foo.bar"), [])

    def test_read_in_file_with_empty_input_file(self):
        data = ""
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True):
            self.assertEqual(read_in_file("foo.bar"), [])
			
    def test_read_in_file_for_open_with_IOError(self):
        data = self.URL_VALID_IMAGE_1 + '\n' + self.URL_VALID_IMAGE_2
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True) as mock_file:
            mock_file.side_effect = IOError
            self.assertEqual(read_in_file("foo.bar"), [])
			
    # download_by_text_file ##################################################
	
    def test_download_by_text_file_with_empty_list(self):
        data = ''
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True):
            self.assertEqual(download_by_text_file("foo.bar"), 0)
		
    def test_download_by_text_file_with_valid_image_urls(self):
        data = self.URL_VALID_IMAGE_1 + '\n' + self.URL_VALID_IMAGE_2
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True):
            url_list = read_in_file("foo.bar")
        self.assertEqual(download_by_url_list(url_list), 2)			

    def test_download_by_text_file_with_broken_image_urls(self):
        data = self.URL_BROKEN_LINK + '\n' + self.URL_VALID_IMAGE_2
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True):
            url_list = read_in_file("foo.bar")
        self.assertEqual(download_by_url_list(url_list), 1)
		
    def test_download_by_text_file_with_invalid_image_format(self):
        data = self.URL_INVALID_IMAGE + '\n' + self.URL_VALID_IMAGE_2
        fake_file = io.StringIO(data)
        with patch('builtins.open', return_value=fake_file, create=True):
            url_list = read_in_file("foo.bar")
        self.assertEqual(download_by_url_list(url_list), 1)
			
if __name__ == '__main__':
    unittest.main()