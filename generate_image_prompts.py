"""
Generate Image Prompts Script

This script generates descriptive prompts for creating images tailored to specific use cases. 
Prompts are generated using a pre-trained model and can be guided by a user-provided image 
or a default white image.

Features:
- Generate prompts for specific styles or themes (e.g., "children's drawings", "vintage Polaroid photographs").
- Accept a single representative image to guide prompt generation or use a default white image.
- Specify the number of prompts and output file location.

Example Usage:
1. Using a Representative Image:
    python generate_image_prompts.py --use-case "children's drawings with vibrant colors" --num-prompts 5 --output-file prompts.json --temp-image /path/to/example_image.jpg

2. Using a Default White Image:
    python generate_image_prompts.py --use-case "children's drawings with vibrant colors" --num-prompts 5 --output-file prompts.json

Arguments:
- --use-case (str): The style or theme for the generated prompts (required).
- --num-prompts (int): The number of prompts to generate (default: 10).
- --output-file (str): Path to save the generated prompts as a JSON file (required).
- --temp-image (str): Path to a single image that represents the benchmark (optional). 
                      If not provided, a white image is automatically created and used.

Requirements:
- Install required dependencies:
    pip install -r requirements.txt

- Set your Replicate API token as an environment variable:
    export REPLICATE_API_TOKEN="your_api_token_here"

Output:
- The generated prompts are saved as a JSON file at the specified location.

Example Output (JSON):
[
    "children's drawings with vibrant colors, showcasing their artistic talents and creativity. The drawings are filled with a variety of vivid hues, including reds, greens, blues, and yellows, creating a lively and energetic atmosphere.",
    "a cheerful drawing featuring a bright sun and colorful shapes, radiating warmth and playfulness.",
    "a colorful depiction of a rainbow over a green field, created with vibrant strokes and lively details."
]

License:
This script is licensed under the MIT License.
"""

import replicate
import argparse
import json
from PIL import Image
import os

def create_white_image(image_path):
    """
    Create a white image of size 256x256 pixels.
    This image serves as a default input when no specific image is provided.

    Args:
        image_path (str): Path to save the created white image.
    """
    img = Image.new('RGB', (256, 256), color='white')
    img.save(image_path)
    print(f"White image created at {image_path}")

def generate_image_prompts(use_case, num_prompts, output_file, temp_image):
    """
    Generate creative image prompts based on the specified use case.
    Prompts are generated using a pre-trained model with the given image as input.

    Args:
        use_case (str): Description of the style or type of images to generate prompts for.
        num_prompts (int): Number of prompts to generate.
        output_file (str): Path to save the generated prompts as a JSON file.
        temp_image (str): Path to the image to be used as input to the model.

    Output:
        A JSON file containing the generated prompts.
    """
    # Initialize the Replicate client
    client = replicate.Client()
    prompts = []

    for _ in range(num_prompts):
        # Use the model to generate a prompt
        output = replicate.run(
            "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
            input={
                "image": open(temp_image, "rb"),  # Input image (white or user-provided)
                "top_p": 0.9,
                "temperature": 0.7,
                "prompt": f"""
                Create a creative and descriptive prompt for generating an image that fits the following use case:
                "{use_case}".
                The prompt should directly describe the image content in a way that can be used to create an image, focusing on visual elements, color, and atmosphere. Do not include phrases like 'The image features' or any commentary about the image. Only output the prompt.
                """,
                "max_tokens": 100
            }
        )
        description = ''.join(output).strip()  # Ensure clean output
        prompts.append(description)
        print(f"Generated prompt: {description}")

    # Save the generated prompts to a JSON file
    with open(output_file, "w") as f:
        json.dump(prompts, f, indent=4)
    print(f"Generated {len(prompts)} prompts saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate prompts for creating images.")
    parser.add_argument("--use-case", required=True, help="The style or use case for the generated prompts (e.g., children's drawings, vintage Polaroid).")
    parser.add_argument("--num-prompts", type=int, default=10, help="Number of prompts to generate (default: 10).")
    parser.add_argument("--output-file", required=True, help="Path to save the generated prompts as JSON.")
    parser.add_argument("--temp-image", help="Path to a single image file that represents the benchmark you want to generate. If not provided, a white image will be created and used.")
    args = parser.parse_args()

    # Determine the image to use
    if args.temp_image:
        if not os.path.exists(args.temp_image):
            print(f"Error: The specified image path does not exist: {args.temp_image}")
            exit(1)
        print(f"Using provided image at {args.temp_image}")
        temp_image = args.temp_image
    else:
        # Create a white image if no image is provided
        temp_image = "white_image.jpg"
        create_white_image(temp_image)

    # Generate prompts
    generate_image_prompts(args.use_case, args.num_prompts, args.output_file, temp_image)

    # Clean up the white image if it was created
    if temp_image == "white_image.jpg" and os.path.exists(temp_image):
        os.remove(temp_image)
        print(f"Temporary image {temp_image} deleted.")
