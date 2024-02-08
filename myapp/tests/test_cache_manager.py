import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock, patch
from cache.cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):
    @patch('cache.cache_manager.redis.Redis', autospec=True)
    def test_set(self, mock_redis):
        CacheManager._instance = None
        cache_manager = CacheManager()
        cache_manager.set('key', 'value')
        mock_redis.return_value.set.assert_called_once_with('key', 'value')

    @patch('cache.cache_manager.redis.Redis', autospec=True)
    def test_get(self, mock_redis):
        CacheManager._instance = None
        cache_manager = CacheManager()
        cache_manager.get('key')
        mock_redis.return_value.get.assert_called_once_with('key')

if __name__ == "__main__":
    unittest.main()