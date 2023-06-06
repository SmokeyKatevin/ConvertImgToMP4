import os, sys, cv2
from tqdm import tqdm

def create_video_from_images(file_name, path, destination_folder):
    """
    Creates a video from a folder of images.

    Args:
        file_name (str): name of the output video file.
        path (str): path to the folder containing the images.
        destination_folder (str): path to the folder where the output video file will be saved.

    Returns:
        None
    """

    # If file_name is not provided, set it to "none"
    if file_name is None:
        file_name = "none"
    
    # If destination_folder is not provided, set it to the root path of the given path
    if destination_folder is None:
        destination_folder = os.path.dirname(path)
    
    # Create output video file path
    output_path = os.path.join(destination_folder, f"{file_name}.mp4")

    # Get all image files from the specified path and its subfolders
    image_files = get_image_files(path)
    
    # Get the dimensions of the first image file
    first_image = cv2.imread(image_files[0])
    height, width, _ = first_image.shape
    
    # Define the output video properties
    output_width = 2560
    output_height = 1440
    output_fps = 60

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_path, fourcc, output_fps, (output_width, output_height))
    
    # Create a progress bar
    progress_bar = tqdm(total=len(image_files), unit="frame")

    # Iterate over each image file and add it as a frame to the video
    for image_file in image_files:
        image = cv2.imread(image_file)
        
        # Resize the image while preserving aspect ratio
        resized_image = resize_image(image, output_width, output_height)
        
        # Write the resized image to the video
        video_writer.write(resized_image)
        
        # Update the progress bar
        progress_bar.update(1)
    
    # Release the video writer and destroy any remaining windows
    video_writer.release()
    cv2.destroyAllWindows()
    
    progress_bar.close()
    print(f"Video created successfully at: {output_path}")

def get_image_files(path):
    """
    Returns a list of all image files in the specified path and its subfolders.

    Args:
        path (str): path to the folder containing the images.

    Returns:
        list: list of all image files in the specified path and its subfolders.
    """
    image_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files.append(os.path.join(root, file))
    return image_files

def resize_image(image, width, height):
    """
    Resizes an image while preserving aspect ratio.

    Args:
        image (numpy.ndarray): image to be resized.
        width (int): desired width of the image.
        height (int): desired height of the image.

    Returns:
        numpy.ndarray: resized image.
    """
    aspect_ratio = min(width / image.shape[1], height / image.shape[0])
    new_width = int(image.shape[1] * aspect_ratio)
    new_height = int(image.shape[0] * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    padding_width = int((width - new_width) / 2)
    padding_height = int((height - new_height) / 2)
    padded_image = cv2.copyMakeBorder(resized_image, padding_height, padding_height, padding_width, padding_width, cv2.BORDER_CONSTANT)
    return padded_image

if __name__ == "__main__":
    # Extract the command-line arguments
    file_name = sys.argv[1] if len(sys.argv) > 1 else None
    path = sys.argv[2]
    destination_folder = sys.argv[3] if len(sys.argv) > 3 else None

    # Call the function to create the video from images
    create_video_from_images(file_name, path, destination_folder)

    # Example usage:
    # python create_video_from_images.py "video" "C:\Users\user\Desktop\images" "C:\Users\user\Desktop\videos"