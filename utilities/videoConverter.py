from moviepy import VideoFileClip
import os

def convertVideo(videoPath, destinationFolder):
    filename = os.path.basename(videoPath)
    name, _ = os.path.splitext(filename)

    outputPath = os.path.join(destinationFolder, name + ".mp4")

    clip = VideoFileClip(videoPath)
    clip.write_videofile(
        outputPath,
        codec="libx264",
        audio_codec="aac"
    )
    clip.close()


def batchConvertVideo(folderPath, destinationPath):
    os.makedirs(destinationPath, exist_ok=True)

    for filename in os.listdir(folderPath):
        if filename.lower().endswith(".mov"):
            convertVideo(
                os.path.join(folderPath, filename),
                destinationPath
            )
