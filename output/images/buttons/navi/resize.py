from PIL import Image
import os

# Function to resize an image based on the relative difference in resolutions
def resize_image(input_path, output_folder, original_resolution, target_resolution):
    # Calculate the scaling factor for width and height
    width_scale = target_resolution[0] / original_resolution[0]
    height_scale = target_resolution[1] / original_resolution[1]

    # Open the image
    with Image.open(input_path) as img:
        # Calculate the new size based on scaling factors
        new_width = int(img.width * width_scale)
        new_height = int(img.height * height_scale)

        # Resize the image with Lanczos resampling for antialiasing
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        # Extract the original file name (without extension)
        original_filename = os.path.splitext(os.path.basename(input_path))[0]

        # Construct the output file name based on resolution and original file name
        output_filename = f"{target_resolution[0]}x{target_resolution[1]}_{original_filename}.png"
        
        # Construct the full output path
        output_path = os.path.join(output_folder, output_filename)

        # Save the resized image
        resized_img.save(output_path)

# Specify the target resolutions
target_resolutions = [
    (4096, 2160),
    (3840, 2160),
    (3840, 1080),
    (2560, 1600),
    (2560, 1600),
    (2560, 1440),
    (2560, 1080),
    (2048, 1536),
    (1920, 1440),
    (1920, 1080),
    (1856, 1392),
    (1680, 1050),
    (1600, 1200)
]

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Iterate through all files in the script's directory
for filename in os.listdir(script_dir):
    if filename.endswith(".png"):
        input_path = os.path.join(script_dir, filename)

        # Extract the original file name (without extension) here
        original_filename = os.path.splitext(os.path.basename(input_path))[0]

        # Iterate through target resolutions
        for resolution in target_resolutions:
            output_folder = os.path.join(script_dir, f"{resolution[0]}x{resolution[1]}")
            
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Replace these with the actual original and target resolutions
            original_resolution = (3840, 2160)  # Example original resolution
            resize_image(input_path, output_folder, original_resolution, resolution)

            print(f"Resized {filename} to {resolution[0]}x{resolution[1]} and saved as {output_folder}/{resolution[0]}x{original_filename}.png.")
