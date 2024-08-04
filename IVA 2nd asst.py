# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 15:24:45 2024

@author: RADHASHYAM
"""
#Lab Task 1: Setup and Basic Extraction
#Objective:
#Install the necessary tools and libraries, and extract frame information from a video.
#Steps:
#1.	Install ffmpeg and ffmpeg-python:
#o	Install the ffmpeg tool and the ffmpeg-python library.
#2.	Extract Frame Information:
#Extract frame information from a sample video

import ffmpeg

def extract_frame_info(video_path):
    try:
        # Probe the video to get detailed information
        probe = ffmpeg.probe(video_path)

        # Extract video stream information
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        if video_stream is None:
            print('No video stream found in the file.')
        else:
            width = video_stream['width']
            height = video_stream['height']
            codec = video_stream['codec_name']
            frame_rate = eval(video_stream['r_frame_rate'])
            duration = float(video_stream['duration'])

            print(f'Video Width: {width}')
            print(f'Video Height: {height}')
            print(f'Codec: {codec}')
            print(f'Frame Rate: {frame_rate}')
            print(f'Duration: {duration} seconds')

    except ffmpeg.Error as e:
        print(f'Error: {e.stderr.decode()}')

if __name__ == "__main__":
    video_path = 'C://Users//RADHASHYAM//Downloads//video.mp4'
    extract_frame_info(video_path)

#Lab Task 2: Frame Type Analysis
#Objective:
#Analyze the extracted frame information to understand the distribution of I, P, and B frames in a video.
#Steps:
#1.	Modify the Script:
#o	Count the number of I, P, and B frames.
#o	Calculate the percentage of each frame type in the video.
#2.	Analyze Frame Distribution:
#o	Plot the distribution of frame types using a library like matplotlib.
#o	Plot a pie chart or bar graph showing the distribution of frame types using matplotlib.

import matplotlib.pyplot as plt

def get_frame_counts(video_path):
    # Run ffprobe to get video stream information
    probe = ffmpeg.probe(video_path,select_streams='v', show_frames=None, show_entries='frame=pict_type')
    frames = probe['frames']

    # Initialize counts for each frame type
    counts = {'I': 0, 'P': 0, 'B': 0}
    for frame in frames:
        frame_type = frame.get('pict_type', 'Unknown')
        if frame_type in counts:
            counts[frame_type] += 1

    total = sum(counts.values())
    percentages = {key: (value / total) * 100 for key, value in counts.items()}

    # Output frame type counts and percentages
    print(f"I-Frames: {counts['I']} ({percentages['I']:.2f}%)")
    print(f"P-Frames: {counts['P']} ({percentages['P']:.2f}%)")
    print(f"B-Frames: {counts['B']} ({percentages['B']:.2f}%)")

    return counts, percentages

def visualize_frame_distribution(frame_counts, frame_percentages):
    labels = ['I-Frames', 'P-Frames', 'B-Frames']
    counts = [frame_counts['I'], frame_counts['P'], frame_counts['B']]

    # Bar Chart for frame type counts
    plt.figure(figsize=(10, 5))
    plt.bar(labels, counts, color=['blue', 'green', 'red'])
    plt.xlabel('Frame Type')
    plt.ylabel('Number of Frames')
    plt.title('Distribution of Frame Types')
    plt.show()

    # Pie Chart for frame type percentages
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=['blue', 'green', 'red'])
    plt.title('Frame Type Distribution')
    plt.show()

# Provide the path to your video file
video_path = 'C://Users//RADHASHYAM//Downloads//video.mp4'

# Obtain the frame counts and percentages
frame_counts, frame_percentages = get_frame_counts(video_path)

# Create visualizations for the frame distribution
visualize_frame_distribution(frame_counts, frame_percentages)


#Lab Task 3: Visualizing Frames
#Objective:
#Extract actual frames from the video and display them using Python.
#Steps:
#1.	Extract Frames:
#o	Use ffmpeg to extract individual I, P, and B frames from the video.
#o	Save these frames as image files.
#2.	Display Frames:
#o	Use a library like PIL (Pillow) or opencv-python to display the extracted frames.
#Tasks:
#1.	Save I, P, and B frames as separate image files using ffmpeg.
#2.	Use PIL or opencv-python to load and display these frames in a Python script.
#3.	Compare the visual quality of I, P, and B frames.

import os
from PIL import Image

# Function to extract specific frame types (I, P, B) and save them as images
def extract_frames_by_type(video_path, output_folder, frame_type):
    os.makedirs(output_folder, exist_ok=True)
    try:
        (
            ffmpeg
            .input(video_path)
            .output(f'{output_folder}/frame_%04d.png', vf=f'select=eq(pict_type\\,{frame_type})', vsync='vfr')
            .run()
        )
        print(f"{frame_type} frames extracted and saved to {output_folder}")
    except Exception as e:
        print(f"Error extracting {frame_type} frames: {e}")
        
# Function to display frames using PIL (Pillow)
def display_frames(folder_path):
    image_files = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith('.png')]
    for image_file in image_files:
        img = Image.open(image_file)
        img.show()

video_path = 'C://Users//RADHASHYAM//Downloads//video.mp4'

# Output directories for I, P, and B frames
output_folders = {
    'I': 'C://Users//RADHASHYAM//Downloads//I_frames',
    'P': 'C://Users//RADHASHYAM//Downloads//P_frames',
    'B': 'C://Users//RADHASHYAM//Downloads//B_frames'
}

# Extract and display I, P, and B frames
for frame_type, folder in output_folders.items():
    extract_frames_by_type(video_path, folder, frame_type)
    display_frames(folder)
    
#Lab Task 4: Frame Compression Analysis
#Objective:
#Analyze the compression efficiency of I, P, and B frames.
#Steps:
#1.	Calculate Frame Sizes:
#o	Calculate the file sizes of extracted I, P, and B frames.
#o	Compare the average file sizes of each frame type.
#2.	Compression Efficiency:
#o	Discuss the role of each frame type in video compression.
#o	Analyze why P and B frames are generally smaller than I frames.

# Function to calculate the size of a file in bytes
def calculate_file_size(file_path):
    return os.path.getsize(file_path)

# Function to calculate the average size of frames in a folder
def calculate_average_frame_size(folder_path):
    frame_sizes = []
    for frame_file in os.listdir(folder_path):
        if frame_file.endswith('.png'):  # Assuming frames are saved as .png
            frame_path = os.path.join(folder_path, frame_file)
            frame_size = calculate_file_size(frame_path)
            frame_sizes.append(frame_size)
    average_size = sum(frame_sizes) / len(frame_sizes) if frame_sizes else 0
    return average_size, frame_sizes

# Paths to the extracted frames (replace these with your paths)
i_frames_folder = 'C://Users//RADHASHYAM//Downloads//I_frames'
p_frames_folder = 'C://Users//RADHASHYAM//Downloads//P_frames'
b_frames_folder = 'C://Users//RADHASHYAM//Downloads//B_frames'

# Calculate average frame sizes
i_avg_size, i_frame_sizes = calculate_average_frame_size(i_frames_folder)
p_avg_size, p_frame_sizes = calculate_average_frame_size(p_frames_folder)
b_avg_size, b_frame_sizes = calculate_average_frame_size(b_frames_folder)

# Print results
print(f"Average I-Frame Size: {i_avg_size / 1024:.2f} KB")
print(f"Average P-Frame Size: {p_avg_size / 1024:.2f} KB")
print(f"Average B-Frame Size: {b_avg_size / 1024:.2f} KB")


#Lab Task 5: Advanced Frame Extraction
#Objective:
#Extract frames from a video and reconstruct a part of the video using only I frames.
#Steps:
#1.	Extract and Save I Frames:
#o	Extract I frames from the video and save them as separate image files.
#2.	Reconstruct Video:
#o	Use the extracted I frames to reconstruct a portion of the video.
#o	Create a new video using these I frames with a reduced frame rate.

import subprocess

def reconstruct_video_from_i_frames(i_frames_folder, output_video_path, frame_rate=30):
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("FFmpeg is not installed or not found in the system path.")
    if not os.path.isdir(i_frames_folder):
        raise FileNotFoundError(f"The directory {i_frames_folder} does not exist.")
    i_frames = [f for f in os.listdir(i_frames_folder) if os.path.isfile(os.path.join(i_frames_folder, f))]
    if not i_frames:
        raise FileNotFoundError(f"No files found in the directory {i_frames_folder}.")
    i_frames.sort()
    with open('frames_list.txt', 'w') as file:
        for frame in i_frames:
            file.write(f"file '{os.path.join(i_frames_folder, frame)}'\n")
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'frames_list.txt',
        '-framerate', str(frame_rate),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_video_path
    ]

    subprocess.run(command, check=True)
    os.remove('frames_list.txt')
i_frames_folder = 'C:\\Users\\RADHASHYAM\\Downloads\\I_frames'
output_video_path = 'C:\\Users\\RADHASHYAM\\Downloads\\output_reconstructed_video.mp4'
reconstruct_video_from_i_frames(i_frames_folder, output_video_path, frame_rate=15)