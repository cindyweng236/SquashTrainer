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

def main():
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    source_root = os.path.join(workspace_root, "source_videos")
    landmark_output_root = os.path.join(workspace_root, "landmark_data")
    fps_output_root = os.path.join(workspace_root, "fps_data")

    video_roots = [
        os.path.join(source_root, "backhand"),
        os.path.join(source_root, "forehand"),
    ]

    valid_extensions = {".mp4"}

    for video_root in video_roots:
        if not os.path.isdir(video_root):
            continue

        for current_dir, _, filenames in os.walk(video_root):
            relative_dir = os.path.relpath(current_dir, source_root)
            path_parts = relative_dir.split(os.sep)
            if path_parts and path_parts[-1] in {"mp4", "original"}:
                path_parts = path_parts[:-1]

            landmark_output_dir = os.path.join(landmark_output_root, *path_parts)
            fps_output_dir = os.path.join(fps_output_root, *path_parts)
            os.makedirs(landmark_output_dir, exist_ok=True)
            os.makedirs(fps_output_dir, exist_ok=True)

            for filename in filenames:
                if os.path.splitext(filename)[1] not in valid_extensions:
                    continue

                video_path = os.path.join(current_dir, filename)
                base_name = os.path.splitext(filename)[0]
                output_name = base_name + ".npy"
                landmark_output_path = os.path.join(landmark_output_dir, output_name)
                fps_output_path = os.path.join(fps_output_dir, base_name + "_fps.json")

                print(f"Processing {video_path} -> {landmark_output_path}, {fps_output_path}")
                all_frames = extract_landmarks(video_path, landmark_output_path)
                extract_fps(video_path, fps_output_path, num_frames=len(all_frames))


if __name__ == "__main__":
    main()