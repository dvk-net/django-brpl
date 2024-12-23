import utils
from unittest.mock import mock_open, patch
from pathlib import Path

class TestDjangoSettings:
    
    def test_extract_secret_from_settings_5_1_3(self, django_settings_5_1_3):
        mock_data = django_settings_5_1_3
        mock_open_obj = mock_open(read_data=mock_data)
        with patch('builtins.open', mock_open_obj):
            result = utils.extract_secret_from_settings(Path(__file__).resolve().parent)
        assert result == "SECRET_KEY = 'django-insecure-1$$7^45i$-!*ny$^vs25xf7cbx2sxskap88x^^jyn6$zr7@+s1'\n"

    def test_update_settings_file_5_1_3(self, django_settings_5_1_3, django_settings_5_1_3_modified):
        mock_data = django_settings_5_1_3
        mock_open_obj = mock_open(read_data=mock_data)
        with patch('builtins.open', mock_open_obj):
            utils.update_settings_file(Path(__file__).resolve().parent)
        mock_open_obj().write.assert_called_once_with(django_settings_5_1_3_modified)