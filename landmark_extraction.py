import cv2
import json
import mediapipe as mp
import numpy as np
import os

def get_video_fps(video_path, fallback_fps=30.0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    if fps <= 0:
        if fallback_fps is None:
            raise ValueError(f"Invalid FPS ({fps}) for video: {video_path}")
        print(f"Warning: invalid FPS ({fps}) for {video_path}; using fallback {fallback_fps}")
        return float(fallback_fps)

    return float(fps)

def extract_fps(video_path, output_path, num_frames, fallback_fps=30.0):
    fps = get_video_fps(video_path, fallback_fps)
    fps_data = {
        "fps": float(fps),
        "num_frames": int(num_frames),
        "video_path": str(video_path),
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fps_data, f, indent=4)
    return fps

def extract_landmarks(video_path, output_path):
    cap = cv2.VideoCapture(video_path)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    all_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb)

        frame_landmarks = []
        if results.pose_landmarks:
            # 33 landmarks
            for landmark in results.pose_landmarks.landmark:
                frame_landmarks.append([
                    landmark.x,
                    landmark.y,
                    landmark.z,
                    landmark.visibility
                ])
        else:
            frame_landmarks = [[np.nan] * 4 for _ in range(33)]
        all_frames.append(frame_landmarks)

    cap.release()
    pose.close()

    # Shape: (num_frames, 33, 4)
    all_frames = np.array(all_frames)

    print(all_frames.shape)

    np.save(output_path, all_frames)


    return all_frames