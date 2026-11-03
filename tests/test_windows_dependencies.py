"""Dependency integrity checks use local in-memory downloads, never the network."""
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.prepare_windows_dependencies import verified_download


class WindowsDependenciesTests(unittest.TestCase):
    def test_verified_cache_does_not_download(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'payload'
            target.write_bytes(b'official')
            with patch('urllib.request.urlopen') as download:
                verified_download({'sha256': hashlib.sha256(b'official').hexdigest()}, target)
                download.assert_not_called()

    def test_mismatch_preserves_old_file_and_removes_partial(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'payload'
            target.write_bytes(b'old')
            spec = {'url': 'https://example.invalid/dependency', 'sha256': hashlib.sha256(b'official').hexdigest()}
            with patch('urllib.request.urlopen', return_value=io.BytesIO(b'tampered')):
                with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                    verified_download(spec, target)
            self.assertEqual(target.read_bytes(), b'old')
            self.assertFalse(target.with_suffix('.download').exists())

    def test_success_replaces_corrupt_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'payload'
            target.write_bytes(b'corrupt')
            spec = {'url': 'https://example.invalid/dependency', 'sha256': hashlib.sha256(b'official').hexdigest()}
            with patch('urllib.request.urlopen', return_value=io.BytesIO(b'official')):
                verified_download(spec, target)
            self.assertEqual(target.read_bytes(), b'official')


if __name__ == '__main__':
    unittest.main()
