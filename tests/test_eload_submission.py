import os
from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch

from eva_submission import ROOT_DIR, __version__
from eva_submission.eload_submission import Eload
from eva_submission.submission_config import EloadConfig, load_config


class TestEload(TestCase):
    resources_folder = os.path.join(ROOT_DIR, 'tests', 'resources')

    def setUp(self):
        config_file = os.path.join(self.resources_folder, 'submission_config.yml')
        load_config(config_file)
        # Need to set the directory so that the relative path set in the config file works from the top directory
        os.chdir(ROOT_DIR)
        self.eload = Eload(55)
        self.original_config = EloadConfig(os.path.join(self.eload.eload_dir, 'original_config.yml'))
        self.updated_config = EloadConfig(os.path.join(self.eload.eload_dir, 'updated_config.yml'))
        # Setup the config
        self.eload.eload_cfg.content = deepcopy(self.original_config.content)
        self.original_updated_cfg = deepcopy(self.updated_config.content)
        self.updated_config.set('version', value=__version__)

    def tearDown(self):
        self.updated_config.content = self.original_updated_cfg
        # remove the config and its backup
        for file_path in [self.eload.eload_cfg.config_file, f'{self.eload.eload_cfg.config_file}.1']:
            print(file_path)
            print(os.path.exists(file_path))
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_create_log_file(self):

        # Creating a second eload object
        self.eload2 = Eload(55)

        logfile_name = os.path.join(self.eload.eload_dir, str(self.eload.eload_num), "submission.log")
        assert os.path.exists(logfile_name)

        self.eload.info("Testing the creation of logging file")
        self.eload2.info("Testing the creation of logging file")

        with open("logfile_name", "r") as test_logfile:
            assert test_logfile.readline().startswith("Testing the creation of logging file")
            assert test_logfile.readlines().count("Testing the creation of logging file\n")==1

    def test_upgrade_config(self):
        """Tests config upgrade for a post-brokering config."""
        self.eload.upgrade_config_if_needed('analysis alias')
        self.assertEqual(self.updated_config.content, self.eload.eload_cfg.content)

    def test_upgrade_config_no_analysis_alias_passed(self):
        """If no analysis alias is passed, it should retrieve from metadata when possible."""
        with patch('eva_submission.config_migration.EvaXlsxReader') as mock_reader:
            mock_reader.return_value.analysis = [{'Analysis Alias': 'analysis alias'}]
            self.eload.upgrade_config_if_needed(analysis_alias=None)
            self.assertEqual(self.updated_config.content, self.eload.eload_cfg.content)

    def test_upgrade_config_already_updated(self):
        """An already up-to-date config shouldn't get modified."""
        original_content = deepcopy(self.updated_config.content)
        self.eload.upgrade_config_if_needed('analysis alias')
        self.assertEqual(original_content, self.updated_config.content)
