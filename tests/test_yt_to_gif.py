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

@patch("src.yt_to_gif.YouTube")
def test_download_video_mocked(mock_yt, temp_dir):
    mock_stream = mock_yt.return_value.streams.filter.return_value.get.highest_resolution.return_value
    mock_stream.download.return_value = str(temp_dir / "downloaded_video.mp4")
    
    downloaded_path = download_video("https://NOT_A_REAL_URL")
    assert downloaded_path.endswith(".mp4")
    assert os.path.exists(downloaded_path)



@patch("subprocess.run")
def test_slice_video_mocked(mock_run, temp_dir): 
    input_file = str(temp_dir / ".mp4")
    with open(input_file, "w") as f:
        f.write("not actually video data")
        
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
    
    
    
