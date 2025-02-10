# yt_url_to_gif

A CLI utility written in Python 3.12.3 that downloads a section of a youtube video and converts it to a gif using the following dependencies:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download YouTube videos  
- A locally packaged [FFmpeg](https://ffmpeg.org/) binary to slice and convert clips

The script accepts three arguments:  
1. **YouTube Video URL**  
2. **Start Time** (in `MM:SS` format)  
3. **Stop Time** (in `MM:SS` format)

It then:
1. Downloads the specified YouTube video (MP4 preferred).  
2. Slices a portion from the provided start time to stop time.  
3. Converts the sliced clip to a GIF.  

---

## Features

- Uses yt-dlp for reliable YouTube downloads.  
- Allows specifying start/end times in `MM:SS`.  
- Relies on locally packaged FFmpeg binaries under `bin/<platform>/`.  
- Can automatically remove intermediate MP4 files after GIF creation.

---

## Current Known Issues

- The spliced mp4 file remains in the directory where the program is run. This needs to be removed to leave only the .gif
- Only AMD64 linux ffmpeg binary is included under bin/  
- Audio only splice / empty splice download . Need to add error handling and/or more verbose error handling

## Project Layout (truncated)

```text
yt_url_to_gif/
├── bin/
│   ├── linux/
│   │   └── ffmpeg
│   └── windows/
│       └── ffmpeg.exe
├── src/
│   └── yt_to_gif.py
└── tests/
    └── test_yt_to_gif.py
```

- `bin`: Contains FFMpeg binaries
- `src/yt_to_gif.py`: Main script
- `tests/test_yt_to_gif.py`: Unit and integration test (uses `pytest`). Integration test uses a working youtube download link for testing. This may fail if the youtube link becomes stale.


## Installation

1. Clone this repo:
```bash
git clone https://github.com/columbladee/yt-url-to-gif.git
cd yt-url-to-gif
```
2. Set up python venv
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

While still in venv (e.g. `source venv/bin/activate`) run
```bash
python3 src/yt_to_gif.py "<Youtube_Url>" <start_time> <stop_time>
```
- `<Youtube_Url>` - URL of youtube video you want a gif from
- `<start_time>` - GIF start time in MM:SS
- `<start_time>` - GIF end time in MM:SS

Example:
```bash
python src/yt_to_gif.py "https://www.youtube.com/watch?v=SiMHTK15Pik" 00:30 00:40
```

This takes the video URL above and creates a gif beginning at 30 seconds and ending at 40 seconds in the video.

## Testing

1.  **Make sure you have the dependencies installed, you will need pytest**: `pip install requirements.txt`

2. **Make sure you're using the venv environment like you're using the program**: `source venv/bin/activate`

3. Run the following:
```bash
python3 -m pytest -v
```
You can safely ignore the warning about the `@pytest.mark.integration` mark. 

## README Unfinished, expect more

