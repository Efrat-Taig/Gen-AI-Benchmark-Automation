import replicate
import re
import argparse
import json
import os
import shutil
from PIL import Image

# Set up your Replicate API key as an environment variable

os.environ["REPLICATE_API_TOKEN"] = "API_TOKEN"
API_TOKEN = "API_TOKEN"
client = replicate.Client(api_token=API_TOKEN)

def evaluate_image_with_llava(image_path, use_case):
    """
    Evaluate an image using the LLaVA model via Replicate API.

    Args:
        image_path (str): Path to the image to be evaluated.
        use_case (str): The use case or style (e.g., "children's drawings").

    Returns:
        dict: Scores for each question and the average score.
    """
    questions = [
        f"On a scale from 1 to 10, how well does this image match the style of '{use_case}'?",
        "On a scale from 1 to 10, does this image have the typical visual characteristics of the specified style?",
        f"On a scale from 1 to 10, how likely is it that this image was designed with '{use_case}' in mind?",
        "On a scale from 1 to 10, how closely does this image's color palette match the intended style?"
    ]

    scores = []

    for question in questions:
        print(f"   Asking question: '{question}'")
        response = replicate.run(
            "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
            input={
                "image": open(image_path, "rb"),
                "prompt": question,
                "max_tokens": 50
            }
        )
        try:
            # Concatenate all parts of the generator output into a single string
            response_text = ''.join(list(response)).strip()
            print(f"   Model response: {response_text}")

            # Use regex to extract the first number between 1 and 10
            match = re.search(r'\b([1-9]|10)\b', response_text)
            if match:
                score = int(match.group(1))
                scores.append(score)
            else:
                print(f"   No valid score found in response: {response_text}")
                scores.append(0)  # Default to 0 if no score is found
        except Exception as e:
            print(f"   Error parsing response: {e}")
            scores.append(0)  # Default to 0 on error

    # Calculate the average score
    avg_score = sum(scores) / len(scores)
    print(f"   Final scores: {scores}, Average score: {avg_score:.2f}")

    return {"scores": scores, "average_score": avg_score}

def filter_images_by_score(input_folder, output_folder, use_case, threshold=7):
    """
    Filter images based on evaluation scores and save those that meet the threshold to a new folder.

    Args:
        input_folder (str): Path to the folder containing images to evaluate.
        output_folder (str): Path to the folder where filtered images will be saved.
        use_case (str): The use case or style for evaluation.
        threshold (float): Minimum average score for an image to pass (default: 7).

    Returns:
        None
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\nCreated output folder: {output_folder}")

    images = [f for f in os.listdir(input_folder) if f.endswith((".png", ".jpg", ".jpeg"))]

    print(f"\nFound {len(images)} images in '{input_folder}' for evaluation.\n")

    for image_file in images:
        image_path = os.path.join(input_folder, image_file)

        print(f"Evaluating image: {image_file}\n")

        # Get evaluation scores and average
        evaluation = evaluate_image_with_llava(image_path, use_case)
        avg_score = evaluation["average_score"]

        if avg_score >= threshold:
            # Copy image to the output folder if it meets the threshold
            shutil.copy(image_path, output_folder)
            print(f"\n✅ Image '{image_file}' passed with an average score of {avg_score:.2f}.")
            print(f"   Saved to folder: {output_folder}\n")
        else:
            print(f"\n❌ Image '{image_file}' did not pass. Average score: {avg_score:.2f}.")
            print(f"   This image will not be moved to the output folder.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate images based on a given use case and filter them by score.")
    parser.add_argument("--input-folder", required=True, help="Path to the folder containing images to evaluate.")
    parser.add_argument("--output-folder", default="benchmark_filtered", help="Path to the folder where filtered images will be saved.")
    parser.add_argument("--use-case", required=True, help="The style or use case for evaluation (e.g., 'children's drawings').")
    parser.add_argument("--threshold", type=float, default=7, help="Minimum average score for an image to pass (default: 7).")
    args = parser.parse_args()

    filter_images_by_score(args.input_folder, args.output_folder, args.use_case, args.threshold)
