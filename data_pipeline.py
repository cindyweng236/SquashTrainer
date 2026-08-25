import os
import feature_calculations
import landmark_extraction

def main():
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    source_root = os.path.join(workspace_root, "source_videos")
    landmark_output_root = os.path.join(workspace_root, "landmark_data")
    fps_output_root = os.path.join(workspace_root, "fps_data")
    feature_output_root = os.path.join(workspace_root, "feature_data")

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
            feature_output_dir = os.path.join(feature_output_root, *path_parts)
            os.makedirs(landmark_output_dir, exist_ok=True)
            os.makedirs(fps_output_dir, exist_ok=True)
            os.makedirs(feature_output_dir, exist_ok=True)

            for filename in filenames:
                if os.path.splitext(filename)[1] not in valid_extensions:
                    continue

                video_path = os.path.join(current_dir, filename)
                base_name = os.path.splitext(filename)[0]
                landmark_output_path = os.path.join(landmark_output_dir, base_name + "_landmarks.npy")
                fps_output_path = os.path.join(fps_output_dir, base_name + "_fps.json")
                feature_output_path = os.path.join(feature_output_dir, base_name + "_features.npy")

                print(f"Processing {video_path} -> {landmark_output_path}, {fps_output_path}")
                all_frames = landmark_extraction.extract_landmarks(video_path, landmark_output_path)
                landmark_extraction.extract_fps(video_path, fps_output_path, num_frames=len(all_frames))
                feature_calculations.calculate_features(video_path, feature_output_path)
    
    # feature calculation
    for video_root in video_roots:
        if not os.path.isdir(video_root):
            continue
        


if __name__ == "__main__":
    main()