from moviepy import VideoFileClip

clip = VideoFileClip("squash1.mov")
clip.write_videofile("squash1.mp4", codec="libx264", audio_codec="aac")