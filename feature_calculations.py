import numpy as np

def get_angle(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitudes = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    if magnitudes == 0:
        return 0
    angle = np.arccos(np.clip(dot_product / magnitudes, -1.0, 1.0))
    return np.degrees(angle)

def elbow_angle(isRight, frame, lms):
    #right 12-14-16; left 11-13-15
    #shoulder, elbow, wrist
    target_lm_index = [12, 14, 16] if isRight else [11, 13, 15]
    shoulder = lms[frame, target_lm_index[0], :3]
    elbow = lms[frame, target_lm_index[1], :3]
    wrist = lms[frame, target_lm_index[2], :3]
    
    # Calculate the vectors
    upper_arm = shoulder - elbow
    lower_arm = wrist - elbow

    return get_angle(upper_arm, lower_arm)

def knee_angle(isRight, frame, lms):
    #right 24-26-28; left 23-25-27
    #hip, knee, ankle
    target_lm_index = [24, 26, 28] if isRight else [23, 25, 27]
    hip = lms[frame, target_lm_index[0], :3]
    knee = lms[frame, target_lm_index[1], :3]
    ankle = lms[frame, target_lm_index[2], :3]
    
    # Calculate the vectors
    upper_leg = hip - knee
    lower_leg = ankle - knee

    return get_angle(upper_leg, lower_leg)

def shoulder_line_angle(frame, lms):
    #left shoulder 11, right shoulder 12
    left_shoulder = lms[frame, 11, :2]
    right_shoulder = lms[frame, 12, :2]
    
    # Calculate the vector
    shoulder_vector = right_shoulder - left_shoulder

    return np.degrees(np.arctan2(shoulder_vector[1], shoulder_vector[0]))

def hip_line_angle(frame, lms):
    #left hip 23, right hip 24
    left_hip = lms[frame, 23, :2]
    right_hip = lms[frame, 24, :2]
    
    # Calculate the vector
    hip_vector = right_hip - left_hip

    return np.degrees(np.arctan2(hip_vector[1], hip_vector[0]))

