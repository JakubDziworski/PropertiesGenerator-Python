import argparse
from unittest import TestCase
from properties_generator import *
import mock

class properties_generator_test(TestCase):

    def test_correct_validate_paths_and_country(self):
        self.mockFileExists()
        self.assertIsNone(validatePathsAndCountry("PL","valid_file"))
        self.assertIsNone(validatePathsAndCountry("HU","valid_file"))
        self.assertIsNone(validatePathsAndCountry("RO","valid_file"))
        self.assertIsNone(validatePathsAndCountry("SK","valid_file"))
        self.assertIsNone(validatePathsAndCountry("CZ","valid_file"))
        self.assertIsNone(validatePathsAndCountry("UA","valid_file"))

    def test_bad_file_name(self):
        self.mockFileExists()
        self.assertIsNotNone(validatePathsAndCountry("PL","bad_file"))
        self.assertIsNotNone(validatePathsAndCountry("HU","bad_file"))
        self.assertIsNotNone(validatePathsAndCountry("RO","bad_file"))
        self.assertIsNotNone(validatePathsAndCountry("SK","bad_file"))
        self.assertIsNotNone(validatePathsAndCountry("CZ","bad_file"))
        self.assertIsNotNone(validatePathsAndCountry("UA","bad_file"))

    def test_bad_country(self):
        self.mockFileExists()
        self.assertIsNotNone(validatePathsAndCountry("ES","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("GR","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("BG","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("FDS","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("FG","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("WTf","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("FD","valid_file"))
        self.assertIsNotNone(validatePathsAndCountry("KL","valid_file"))

    def mockFileExists(self):
        path_patcher = mock.patch('os.path.exists')
        mocked_path = path_patcher.start()
        def path_mocker(file_path):
            if file_path == "valid_file": return True
            if file_path == TOMCAT_PATH: return True
            return False
        mocked_path.side_effect = path_mocker


