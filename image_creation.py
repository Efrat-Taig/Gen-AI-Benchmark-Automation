# - A JSON file containing image prompts must exist before running this script.

import json
import os
from diffusers import UNet2DConditionModel, DiffusionPipeline, LCMScheduler
import torch
from PIL import Image

def setup_pipeline():
    '''
    Sets up the diffusion pipeline for generating images.
    The pipeline uses a pre-trained UNet2DConditionModel and a compatible scheduler.

    Returns:
        pipeline (DiffusionPipeline): The configured diffusion pipeline ready for use.
    '''
    # Load the pre-trained UNet2DConditionModel in half-precision (float16) for improved performance on GPUs
    unet = UNet2DConditionModel.from_pretrained("briaai/BRIA-2.3-FAST", torch_dtype=torch.float16)
    
    # Initialize the diffusion pipeline using the UNet model
    pipe = DiffusionPipeline.from_pretrained("briaai/BRIA-2.3-BETA", unet=unet, torch_dtype=torch.float16)
    
    # Allow prompts to contain empty strings without forcing zero vectors
    pipe.force_zeros_for_empty_prompt = False
    
    # Replace the default scheduler with LCMScheduler for better compatibility with the model
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    
    # Move the pipeline to GPU for faster inference
    pipe.to("cuda")
    
    return pipe

def generate_images_from_prompts(prompt_file, output_folder, pipeline, num_inference_steps=8, guidance_scale=1.0):
    '''
    Generates images from prompts using a diffusion pipeline and saves them to the specified folder.

    Args:
        prompt_file (str): Path to the JSON file containing the prompts.
        output_folder (str): Directory where the generated images will be saved.
        pipeline (DiffusionPipeline): The preloaded diffusion pipeline.
        num_inference_steps (int): Number of inference steps for image generation (default: 8).
        guidance_scale (float): A scale factor for controlling prompt adherence (default: 1.0).

    Returns:
        None
    '''
    # Ensure the output directory exists; create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Output folder created: {output_folder}")

    # Load prompts from the JSON file
    with open(prompt_file, "r") as f:
        prompts = json.load(f)
    print(f"Loaded {len(prompts)} prompts from {prompt_file}")

    # Generate images for each prompt
    for i, prompt in enumerate(prompts):
        print(f"Generating image for prompt {i + 1}/{len(prompts)}: {prompt}")
        
        # Use the diffusion pipeline to generate an image from the prompt
        image = pipeline(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

        # Save the generated image to the output folder
        image_path = os.path.join(output_folder, f"image_{i + 1}.png")
        image.save(image_path)
        print(f"Image saved to {image_path}")

if __name__ == "__main__":
    # Define file paths and parameters
    PROMPT_FILE = "generated_prompts.json"  # Path to the JSON file containing prompts
    OUTPUT_FOLDER = "generated_images"      # Directory to save generated images

    # Load the diffusion pipeline
    print("Setting up the diffusion pipeline...")
    pipe = setup_pipeline()
    print("Pipeline is ready.")

    # Generate images based on prompts
    print("Starting image generation...")
    generate_images_from_prompts(PROMPT_FILE, OUTPUT_FOLDER, pipe)
    print("Image generation complete.")
