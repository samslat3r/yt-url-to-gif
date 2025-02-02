import argparse
import subprocess
import os
import platform
from pytube import YouTube

'''
General Workflow:
1) Find FFMPEG
2) Download Video
3) Use FFMPEG to slice the video clip (user defines this as an argument)
4) Use FFMPEG to convert the sliced video to a GIF
5) Clean up sliced video, downloaded video, leaving only the gif.

'''


# Parse time function is to make the beginning and end selections be in mm:ss format instead of HH:MM:SS. 
def parse_time(timestr):

    minutes, seconds = timestr.split(":")
    return int(minutes) * 60 + int(seconds)  

def get_ffmpeg_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    system_name = platform.system().lower() # Win, linux, or darwin. ignore macs, we aren't doing that stuff
    
    if system_name.startswith("win"):
        ffmpeg_binary = os.path.join(current_dir, "..","..","bin","windows","ffmpeg.exe")
    elif system_name.startswith("linux"):
        ffmpeg_binary = os.path.join(current_dir, "..","..","bin","linux","ffmpeg")
    else:
        raise Exception("Unsupported Operating System")
    return ffmpeg_binary

def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()
    downloaded_file = stream.download()
    return downloaded_file

def slice_video(input_file, start_time_str, end_time_str):
    base_name, _ = os.path.splitext(input_file)
    sliced_file = f"{base_name}_sliced.mp4"

    ffmpeg_path = get_ffmpeg_path()
    
    ## To make ffmpeg happy we convert mm:ss => seconds
    start_secs = parse_time(start_time_str)
    end_secs = parse_time(end_time_str)

    slice_command = [
            ffmpeg_path,
            "-i", input_file,
            "-ss", str(start_secs),
            "-to", str(end_secs),
            "-c", "copy",
            sliced_file,
            "-y"
         ]

    subprocess.run(slice_command, check=True)
    return sliced_file

def convert_to_gif(input_file):
    base_name, _ = os.path.splitext(input_file)
    output_gif= f"{base_name}.gif"
    ffmpeg_path = get_ffmpeg_path()

    convert_command = [
            ffmpeg_path,
            "-i", input_file,
            "-vf", "fps=10,scale=640:-1:force_original_aspect_ratio=decrease",
            output_gif,
            "-y"
        ]

    subprocess.run(convert_command, check=True)
    return output_gif

def main():
    parser = argparse.ArgumentParser(
        description="Download a segment of a Youtube video and cmonvert it to a GIF with locally packaged FFMPEG"
    )
    parser.add_argument("url", help="Youtube video URL.")
    parser.add_argument("start_time", help="Start time of the video slice you want in mm:ss like 1:25")
    parser.add_argument("stop_time", help="The time where you want your gif to end.")
    args = parser.parse_args()

    youtube_url = args.url
    start_t = args.start_time
    end_t = args.stop_time
    downloaded_file = download_video(youtube_url)
    sliced_file = slice_video(downloaded_file, start_t, end_t)
    output_gif = convert_to_gif(sliced_file)

    print(f"GIF Created and it seems good: {output_gif}")

if __name__ == "__main__":
    main()
