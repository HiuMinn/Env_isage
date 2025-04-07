import os
from sklearn.model_selection import train_test_split
import random
import time

# root is the directory where the dataset is stored (change this to your dataset path if needed)
# make sure to have the dataset in the correct format as described in the original celeba dataset

tolerance = 10  # Tolerance for checking if the face is facing forward
def filtered_sets(root= "D:/Datasets/", for_test=False, tolerance=tolerance, subset_size=None):

    # Path to the attribute files (needed for filtering)
    attr_file_path = os.path.join(root, 'celeba', 'list_attr_celeba.txt')
    landmarks_file_path = os.path.join(root, 'celeba', 'list_landmarks_align_celeba.txt')
    bbox_file_path = os.path.join(root, 'celeba', 'list_bbox_celeba.txt')

    # Read the attribute file
    with open(attr_file_path, 'r') as f:
        attr_lines = f.readlines()

    # Read the landmarks file
    with open(landmarks_file_path, 'r') as f:
        landmarks_lines = f.readlines()

    # Read the bounding box file
    with open(bbox_file_path, 'r') as f:
        bbox_lines = f.readlines()

    # Extract the attribute names
    attr_names = attr_lines[1].strip().split()

    # Create a dictionary to store the attributes, landmarks, and bounding boxes for each image
    attrs = {}
    for line in attr_lines[2:]:
        parts = line.strip().split()
        img_name = parts[0]
        attributes = list(map(int, parts[1:]))
        attrs[img_name] = {'attributes': attributes}

    for line in landmarks_lines[2:]:
        parts = line.strip().split()
        img_name = parts[0]
        landmarks = list(map(int, parts[1:]))
        if img_name in attrs:
            attrs[img_name]['landmarks'] = landmarks

    for line in bbox_lines[2:]:
        parts = line.strip().split()
        img_name = parts[0]
        bbox = list(map(int, parts[1:]))
        if img_name in attrs:
            attrs[img_name]['bbox'] = bbox

    # Find the indices of the 'Blurry', 'Eyeglasses', and 'Wearing_Hat' attributes
    blurry_idx = attr_names.index('Blurry')
    eyeglasses_idx = attr_names.index('Eyeglasses')
    wearing_hat_idx = attr_names.index('Wearing_Hat')

    # Filter the dataset to include only non-blurry images, without eyeglasses and without wearing hat
    filtered_images = [img for img, attr in attrs.items() if attr['attributes'][blurry_idx] == -1 and attr['attributes'][eyeglasses_idx] == -1 and attr['attributes'][wearing_hat_idx] == -1]

    # Filter images to include only those that are facing forward
    def is_facing_forward(landmarks, bbox):
        lefteye_x, lefteye_y, righteye_x, righteye_y, nose_x, nose_y, leftmouth_x, leftmouth_y, rightmouth_x, rightmouth_y = landmarks
        x1, y1, width, height = bbox
        x2, y2 = x1 + width, y1 + height

        # Check if landmarks are within the bounding box with tolerance
        if not (x1 - tolerance <= lefteye_x <= x2 + tolerance and x1 - tolerance <= righteye_x <= x2 + tolerance and x1 - tolerance <= nose_x <= x2 + tolerance and x1 - tolerance <= leftmouth_x <= x2 + tolerance and x1 - tolerance <= rightmouth_x <= x2 + tolerance):
            return False
        if not (y1 - tolerance <= lefteye_y <= y2 + tolerance and y1 - tolerance <= righteye_y <= y2 + tolerance and y1 - tolerance <= nose_y <= y2 + tolerance and y1 - tolerance <= leftmouth_y <= y2 + tolerance and y1 - tolerance <= rightmouth_y <= y2 + tolerance):
            return False

        # Check if eyes are horizontally aligned and mouth is below the nose
        if abs(lefteye_y - righteye_y) > 10:  # Allow some tolerance
            return False
        if not (nose_y < leftmouth_y and nose_y < rightmouth_y):
            return False

        return True

    filtered_images = [img for img in filtered_images if is_facing_forward(attrs[img]['landmarks'], attrs[img]['bbox'])]

    if subset_size is not None:
        # If subset_size is specified, sample the filtered images
        filtered_images = filtered_images[:subset_size]

    # Divide the filtered images into training, validation, and testing sets
    train_images, test_images = train_test_split(filtered_images, test_size=0.2, random_state=42)

    # Divide the test set into validation and testing sets
    test_images, val_images = train_test_split(test_images, test_size=0.5, random_state=42)

    if for_test:
        # Check the number of attributes
        num_attributes = len(attr_names)
        # Check the number of images
        num_images = len(attrs)
        return train_images, val_images, test_images, filtered_images, num_attributes, num_images
    else:
        return train_images, val_images, test_images
    
if __name__ == "__main__":
    start_time = time.time()
    print("Starting dataset filtering...")
    # Call the function to filter the dataset and split it into training, validation, and testing sets
    train_images, val_images, test_images, filtered_images, num_attributes, num_images = filtered_sets(for_test=True)

    print(f"Number of attributes: {num_attributes}")
    print(f"Number of images: {num_images}")
    print(f"Tolerance for facing forward: {tolerance}")
    print(f"Number of filtered images: {len(filtered_images)}")
    print(f"Number of training images: {len(train_images)}")
    print(f"Number of validation images: {len(val_images)}")
    print(f"Number of testing images: {len(test_images)}")

    # Check for overlapping images between the datasets
    overlap_train_val = set(train_images) & set(val_images)
    overlap_train_test = set(train_images) & set(test_images)
    overlap_val_test = set(val_images) & set(test_images)

    if overlap_train_val:
        print(f"Overlap between training and validation sets: {len(overlap_train_val)} images")
    else:
        print("No overlap between training and validation sets")

    if overlap_train_test:
        print(f"Overlap between training and testing sets: {len(overlap_train_test)} images")
    else:
        print("No overlap between training and testing sets")

    if overlap_val_test:
        print(f"Overlap between validation and testing sets: {len(overlap_val_test)} images")
    else:
        print("No overlap between validation and testing sets")
    
    end_time = time.time()
    print(f"Dataset filtering completed in {end_time - start_time:.2f} seconds")