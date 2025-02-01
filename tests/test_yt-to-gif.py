import unittest
from unittest.mock import patch, Mock, MagicMock
import os
import sys
import subprocess 
from pytube import YouTube
current_dir = os.path.dirname(os.path.abspath(__file__)) #  #only way to import src really such at py_to_gif
src_dir = os.path.join(current_dir, "..", "src")         # only way to get src 
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Have to use `src` instead of `yt-to-gif` because of how the imports work - we are in the `tests` directory
# and need to go up one level to import the `src` module.
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
    #                   mparse_time tests                  #
    ########################################################
    def test_pase_time_valid(self):
        self.assertEqual(parse_time("1:30"), 90)
        self.assertEqual(parse_time("0:30"), 30)
        
    def test_parse_time_invalid(self):
        with self.assertRaises(ValueError):
            parse_time("invalid")
        

    ########################################################
    #                   get_ffmpeg_tests                   #
    ########################################################
    @patch('platform.system')
    def get_ffmpeg_path_windows(self, mock_system):
        mock_system.return_value = "Windows"
        path = get_ffmpeg_path()
        self.assertTrue(path.endswith("bin\\windows\\ffmpeg.exe"))
    
    @patch('platform.system')
    def test_get_ffmpeg_path_linux(self, mock_system):
        mock_system.return_value = "Linux"
        path = get_ffmpeg_path()
        self.assertTrue(path.endswith("bin/linux/ffmpeg"))
        
    @patch('platform.system')
    def test_get_ffmpeg_path_unsupported(self, mock_system):
        mock_system.return_value = "Darwin" # Because we are not gonna support macs dawg
        with self.asserRaises(Exception) as exc:
            get_ffmpeg_path()
        self.assertIn("Unsupported", str(exc.exception))
        
    
    ########################################################
    #                   download video tests               #
    ########################################################
    
    @patch.object(YouTube, 'streams', autospec=True)
    @patch("pytube.YouTube.__init__", return_value=None)
    def test_download_video_success(self, mock_yt_init, mock_streams):
        mock_stream_obj = MagicMock()
        mock_stream_obj.download.return_value = "downloaded_file.mp4"
        mock_streams.filter.return_value.get_highest_resolution.return_value = mock_stream_obj
        
        result = download_video("https://youtu.be/g0X7xpuf_BY")
        self.assertEqual(result, "downloaded_file.mp4")
        mock_stream_obj.download.assert_called_once()
        
    @patch.object(YouTube, 'streams', autospec=True)
    @patch("pytube.YouTube.__init__", return_value=None)
    def test_download_video_network_error(self, mock_yt_init, mock_streams):
        mock_streams.filter.side_effect = Exception("Network Error")
        with self.assertRaises(Exception) as exc:
            download_video("https://youtu.be/g0X7xpuf_BY")
        self.assertIn("Network Error", str(exc.exception))
        
    
    ########################################################
    #                   slice video tests                 #
    ########################################################
    @patch("subprocess.run")
    @patch("yt_to_gif.get_ffmpeg_path", return_value="/path/to/ffmpeg")
    def test_slice_video_normal(self, mock_ffmpeg_path, mock_subprocess):
        input_file = "downloaded_file.mp4"
        start_time = "1:10"
        end_time = "2:00"
        
        output = slice_video(input_file, start_time, end_time)
        self.assertEqual((output, "downloaded_file_sliced.mp4"))
        
        expected_command = [
            "/path/to/ffmpeg",
            "-i", "downloaded_file.mp4",
            "-ss", "70",
            "-to", "120",
            "-c", "copy",
            "downloaded_file_sliced.mp4",
            "-y"
        ]
        mock_subprocess.assert_called_once_with(expected_command, check=True)
        
    @patch("subprocess.run")
    @patch("yt_to_gif.get_ffmpeg_path", return_value="/path/to/ffmpeg")
    def test_slice_to_video_end_before_start(self, mock_ffmpeg_path, mock_subprocess):
        input_file = "downloaded_file.mp4"
        start_time = "2:00"
        end_time = "1:10"
        
        slice_video(input_file, start_time, end_time)
        expected_command = [
            "/path/to/ffmpeg",
            "-i", "downloaded_file.mp4",
            "-ss", "120",
            "-to", "70",
            "-c", "copy",
            "downloaded_file_sliced.mp4",
            "-y"
        ]
        mock_subprocess.assert_called_once_with(expected_command, check=True)
    ########################################################
    #                  convert to gif tests                #
    ########################################################
 
    @patch("subprocess.run")
    @patch("yt_to_gif.get_ffmpeg_path")
    def test_convert_to_gif(self, mock_ffmpeg_path, mock_subprocess):
        mock_ffmpeg_path.return_value = "/path/to/ffmpeg"
        input_file = "downloaded_file_sliced.mp4"
        
        output = convert_to_gif(input_file)
        self.assertEqual(output, "downloaded_file_sliced.gif")
        
        expected_command = [
                "/path/to/ffmpeg",
                "-i", "downloaded_file_sliced.mp4",
                "-vf", "fps=10,scale=640:-1:force_original_aspect_ratio=decrease",
                "downloaded_file_sliced.gif",
                "-y"
        ]
        mock_subprocess.assert_called_once_with(expected_command, check=True)

    ########################################################
    #                 main() tests                         #                  
    ########################################################

@patch("yt_to_gif.download_video", return_value="downloaded_file.mp4")
@patch("yt_to_gif.slice_video", return_value="downloaded_file_sliced.mp4")
@patch("yt_to_gif.convert_to_gif", return_value="downloaded_file_slice.gif")
@patch("sys.argv", ["yt_to_gif.py", "https://youtu.be/g0X7xpuf_BY", "1:00", "2:00"]) 
def test_main(self, mock_gif, 


# function name, link, begin, end
  # https://youtu.be/g0X7xpuf_BY"
   


