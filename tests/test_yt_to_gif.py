import os
import pytest
import shutil
from unittest.mock import patch
from src.yt_to_gif import download_video, slice_video, convert_to_gif
from PIL import Image

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=tWFIIuZNqg4"

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

#------------------------------------------------
# Unit Tests
#------------------------------------------------

@patch("src.yt_to_gif.YoutubeDL")
def test_download_video_mocked(mock_ydl_class, temp_dir):
    # mock instance is used as a context manager
    mock_ydl_instance = mock_ydl_class.return_value.__enter__.return_value
    
    # mock extract_info 
    info_dict_mock = { "title": "Not a real video", "ext": "mp4" }
    mock_ydl_instance.extract_info.return_value = info_dict_mock
    
    # mock prepare_filename
    downloaded_mp4_path = str(temp_dir / "fake_video.mp4")
    mock_ydl_instance.prepare_filename.return_value = downloaded_mp4_path
    
    # Create a dummy file
    with open(downloaded_mp4_path, 'w') as f:
        f.write("dummy content")
    
    # real function call
    downloaded_path = download_video("https://FAKE_URL")
    
    # assertions
    assert downloaded_path.endswith(".mp4")
    assert os.path.exists(downloaded_path), "Download function didn't even create a file" 
    
    mock_ydl_instance.extract_info.assert_called_once_with("https://FAKE_URL", download=True)
    mock_ydl_instance.prepare_filename.assert_called_once_with(info_dict_mock)
 
        

@patch("subprocess.run")
def test_slice_video_mocked(mock_run, temp_dir): 
    input_file = str(temp_dir / "test_input.mp4")
    with open(input_file, "w") as f:
        f.write("this really isn't video data")
        
    output_file = slice_video(input_file, "00:00", "00:10")
    assert output_file.endswith("_sliced.mp4")
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_convert_to_gif_mocked(mock_run, temp_dir):
    input_file = str(temp_dir / "test_sliced.mp4")
    with open(input_file, "w") as f:
        f.write("more fake video data")
        
    output_file = convert_to_gif(input_file)
    assert output_file.endswith(".gif")
    mock_run.assert_called_once()
    
#------------------------------------------------
# Integration Test (Real download, slice, gif)
#------------------------------------------------

@pytest.mark.integration
def test_full_flow_integration(temp_dir):
    
    # Download the video
    downloaded_file = download_video(TEST_VIDEO_URL)
    assert os.path.exists(downloaded_file), "Video didn't download properly."
    
    # Move the video to the temp directory (just to keep things clean)
    downloaded_basename = os.path.basename(downloaded_file)
    new_path = str(temp_dir / downloaded_basename)
    shutil.move(downloaded_file, new_path)
    downloaded_file = new_path
    
    # Slice the first 10 seconds
    sliced_file = slice_video(downloaded_file, "00:00", "00:10")
    assert os.path.exists(sliced_file), "Video didn't slice properly."
    
    # Convert the sliced video to a gif
    output_gif = convert_to_gif(sliced_file)
    assert os.path.exists(output_gif), "GIF didn't convert properly."
    
    # Not mandatory but cool: check file size and metadata (that is, frames, and dimensions)
    with Image.open(output_gif) as img:
        assert img.format == "GIF", "Output isn't a GIF or recognized as a GIF."
        assert img.n_frames >= 1, "GIF has no frames."
        width, height = img.size
        assert width > 0 and height > 0, "GIF has invalid dimensions"
        
    print(f"Integration test GIF created: {output_gif}")
    
    
    
