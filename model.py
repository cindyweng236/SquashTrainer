import cv2
import mediapipe as mp
import numpy as np

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