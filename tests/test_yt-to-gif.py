import unittest
from unittest.mock import patch, MagickMock, mock_open
import os
import sys
import subprocess 
from pytube import YouTube
current_dir = os.path.dirname(os.path.abspath(__file__)) #  #only way to import src really such at py_to_gif
src_dir = os.path.join(current_dir, "..", "src")         # only way to get src 
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


from src import (
    parse_time,
    get_ffmpeg_path,
    download_video,
    slice_video,
    convert_to_gif,
    main
)

class TestYtToGif(unittest.TestCase):
    ########################################################
    #                   pparse_time tests                  #
    ########################################################
    def test_pase_time_valid(self):
        
    def test_parse_time_invalid(self):

    ########################################################
    #                   get_ffmpeg_tests                   #
    ########################################################
    @patch('platform.system')
    def get_ffmpeg_path_windows(self, mock_system):
    
    @patch('platform.system')
    def test_get_ffmpeg_path_unknown(self, mock_system):
        
    @patch('platform.system')
    def test_get_ffmpeg_path_unsupported(self, mock_system):
        
        
    
    ########################################################
    #                   download video tests               #
    ########################################################
    
    ########################################################
    #                   download video tests               #
    ########################################################
    
    ########################################################
    #                  slice video tests                   #
    ########################################################
 
     ########################################################
    #                  main() tests                         #
    #########################################################
 
    
    