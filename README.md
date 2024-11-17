# Gen-AI-Benchmark-Automation

This GitHub repository is an implementation of the article available at the following link:  [paper nameTBD](https://github.com/ZhengPeng7/BiRefNet) 

# **Benchmark Automation for Generative AI**  
This repository provides a complete framework for automating the creation and curation of benchmarks for your specific generative AI use case. I’ve done most of the hard work for you—just customize and run the scripts to build benchmarks tailored to your needs.  

---

## **Features**  
- **Prompt Generation**: Automatically generate custom prompts aligned with your use case.  
- **Image Creation**: Integrates with popular image-generation platforms for fast, high-quality output.  
- **Image Evaluation**: Uses LLaVA (or a similar multi-modal model) to evaluate image relevance to your use case.  
- **Filtering and Curation**: Initial automated filtering, followed by an easy process for manual refinement.  

---

## **How It Works**  

### 1. **Setup**  
Clone this repository

### 2. **Generating Prompts**  
Run the prompt generation script to create prompts tailored to your use case.  

```bash
python generate_prompts.py --use-case "Your Use Case Here"  
```  
This script generates prompts designed to match the specific requirements of your application (e.g., gaming, product photography, etc.).  

### 3. **Creating Images**  
Use the generated prompts to create images with your preferred image-generation platform.  
- For BRIA: Follow the provided API integration example in `image_creation.py`.  
- For other platforms: Update the script with your API key and platform-specific parameters.  

```bash
python image_creation.py --prompts-file prompts.json --output-dir images/  
```

### 4. **Evaluating Images**  
The `evaluate_images.py` script uses LLaVA to evaluate how well the generated images fit your use case.  
- Each image is scored or labeled as "relevant" or "not relevant."  

```bash
python evaluate_images.py --input-dir images/ --output-file evaluation.json  
```

### 5. **Manual Refinement**  
After automated filtering, manually review the remaining images:  
- Use `manual_review.py` to display images and refine your dataset further.  
- This step ensures your benchmark aligns perfectly with your requirements.  

```bash
python manual_review.py --input-file evaluation.json --final-output refined_benchmark/  
```

---

## **Repository Structure**  

- `generate_image_prompts.py`: Generates prompts based on your use case.  
- `image_creation.py`: Creates images using the prompts.  
- `evaluate_images.py`: Evaluates the relevance of generated images using LLaVA or another model.  

---

## **Requirements**  
- Python 3.8+  
- Access to an image-generation API (e.g., BRIA, Stable Diffusion, or another platform).  
- GPU (recommended but not mandatory; options for cloud platforms like Replicate are included).  

---

## **Quick Start with Replicate**  
For users without local GPU access, this repository integrates seamlessly with Replicate:  
1. Create a Replicate account and obtain an API key.  
2. Update `config.json` with your API key.  
3. Follow the instructions for `image_creation.py` to generate images using Replicate’s API.  

---

## **Tips for Best Results**  
- Focus on **quality over quantity**: Curate a smaller dataset that aligns well with your needs.  
- Regularly review and refine prompts and evaluation criteria for improved outputs.  
- Plan your benchmark process carefully to save time in future iterations.  





---
### Example Usage
---
<img src="https://github.com/Efrat-Taig/Gen-AI-Benchmark-Automation/blob/main/img1.png" width="400">

# generate_image_prompts.py

This script generates descriptive prompts for creating images, tailored to specific use cases. The prompts are generated using a pre-trained model, and the input can either be a representative image provided by the user or a default white image.

## Features

- **Custom Use Cases**: Generate prompts for specific styles or themes, such as "children's drawings with vibrant colors" or "vintage Polaroid photographs."
- **Image Input Options**:
  - Use a single representative image to guide the prompt generation.
  - Automatically create and use a white image if no input image is provided.
- **Flexible Parameters**: Customize the number of prompts and output file location.

---

## Usage

The script supports two modes of operation:

### 1. **Using a Representative Image**

Provide a single image that represents the benchmark you want to generate. This image will guide the prompt generation.

```bash
python generate_image_prompts.py --use-case "children's drawings with vibrant colors" --num-prompts 5 --output-file prompts.json --temp-image /path/to/your/example_image.jpg
```

### 2. **Using a Default White Image**

If no representative image is available, the script will create a white image (256x256 pixels) and use it as input.

```bash
python generate_image_prompts.py --use-case "children's drawings with vibrant colors" --num-prompts 5 --output-file prompts.json
```

---

## Arguments

| Argument            | Description                                                                                                     | Required | Default          |
|---------------------|-----------------------------------------------------------------------------------------------------------------|----------|------------------|
| `--use-case`        | The style or use case for the prompts (e.g., "children's drawings", "vintage Polaroid").                       | Yes      | N/A              |
| `--num-prompts`     | Number of prompts to generate.                                                                                 | No       | 10               |
| `--output-file`     | Path to save the generated prompts as a JSON file.                                                             | Yes      | N/A              |
| `--temp-image`      | Path to a single image file that represents the benchmark. If not provided, a white image will be created.     | No       | White image auto-generated |

---

## Output

The generated prompts are saved in a JSON file. Example `prompts.json`:

```json
[
    "children's drawings with vibrant colors, showcasing their artistic talents and creativity. The drawings are filled with a variety of vivid hues, including reds, greens, blues, and yellows, creating a lively and energetic atmosphere.",
    "a cheerful drawing featuring a bright sun and colorful shapes, radiating warmth and playfulness.",
    "a colorful depiction of a rainbow over a green field, created with vibrant strokes and lively details."
]
```

---

## Examples

### Example 1: Use a Representative Image

```bash
python generate_image_prompts.py --use-case "vintage Polaroid photographs" --num-prompts 3 --output-file vintage_prompts.json --temp-image /path/to/vintage_photo.jpg
```

### Example 2: Generate Using a White Image

```bash
python generate_image_prompts.py --use-case "children's drawings with vibrant colors" --num-prompts 5 --output-file vibrant_drawings_prompts.json
```

---

## Notes

- The image provided via `--temp-image` should be a single image that best represents the benchmark you want to build.
- If no image is provided, the script will automatically generate a white image and use it as input.
- Make sure to set your Replicate API token as an environment variable before running the script.

---
<img src="https://github.com/Efrat-Taig/Gen-AI-Benchmark-Automation/blob/main/img2.png" width="400">

# image_creation.py

This script generates high-quality images from textual prompts using a pre-trained diffusion model. It takes prompts from a JSON file, processes them through the model, and saves the resulting images to a specified directory.

## Features

- **Prompt-Based Image Generation**: Creates images directly from descriptive prompts generated by a prior script or written manually.
- **Diffusion Pipeline Setup**: Utilizes a pre-trained diffusion model (`briaai/BRIA-2.3-BETA`) for generating visually stunning and prompt-aligned images.
- **Flexible Parameters**: Customize inference steps and guidance scale to balance quality and computational efficiency.
- **Automatic Output Directory Creation**: Ensures images are saved in a structured and organized manner.

---

## Usage

The script processes prompts stored in a JSON file and generates corresponding images. It assumes you already have a JSON file with prompts, such as one created by the `generate_image_prompts.py` script.

### Example Command

```bash
python generate_images_from_prompts.py --prompt-file prompts.json --output-folder generated_images
```

---

## Arguments

| Argument              | Description                                                                                                     | Required | Default         |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|----------|-----------------|
| `--prompt-file`       | Path to a JSON file containing text prompts. Each prompt describes the visual content to be generated.          | Yes      | N/A             |
| `--output-folder`     | Directory where the generated images will be saved. If it doesn’t exist, it will be created automatically.      | Yes      | N/A             |
| `--num-inference-steps` | Number of diffusion steps for generating each image. Higher values may improve quality at the cost of speed.   | No       | 8               |
| `--guidance-scale`    | Guidance scale controls how closely the images adhere to the prompts. Adjust based on style and clarity.        | No       | 1.0             |

---

## Output

- **Images**:  
  The generated images are saved as `.png` files in the specified output directory. Files are named sequentially, e.g., `image_1.png`, `image_2.png`, etc.

### Example Directory Structure
```
generated_images/
    ├── image_1.png
    ├── image_2.png
    └── image_3.png
```

### Example Prompt File (`prompts.json`)
```json
[
    "A futuristic cityscape at sunset with flying cars.",
    "A serene mountain lake surrounded by pine trees."
]
```

### Corresponding Output Images
1. `image_1.png`: A futuristic cityscape at sunset with flying cars.
2. `image_2.png`: A serene mountain lake surrounded by pine trees.

---

## Example Script Integration

This script is designed to work seamlessly with the `generate_image_prompts.py` script. First, generate a set of prompts using the prior script, then pass the resulting JSON file into this script to produce images.

---

## Notes

- Ensure the diffusion model dependencies are installed:
  ```bash
  pip install diffusers
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```
- Adjust `num-inference-steps` and `guidance-scale` for different styles or computational requirements.
- GPU acceleration is required for efficient image generation. Make sure your environment is properly configured.

---
<img src="https://github.com/Efrat-Taig/Gen-AI-Benchmark-Automation/blob/main/img3.png" width="400">

# evaluate_images.py

#### **Evaluate Images by Style**

This script evaluates a collection of images to determine how well they match a specified style or use case, such as "children's drawings" or "vintage photography." It uses the LLaVA conversational AI model to provide style-related scores, calculates an average score for each image, and filters them based on a threshold.

---

#### **Features**
- **Style Evaluation**:
  - Dynamically evaluates each image by asking multiple questions about its visual style, typical characteristics, color palette, and likelihood of fitting the use case.
- **Score Calculation**:
  - Computes an average score from the LLaVA model’s responses for each image.
- **Automatic Filtering**:
  - Images with an average score above the threshold are copied to a separate folder.
- **Custom Parameters**:
  - Supports input and output folder paths, adjustable thresholds, and custom use cases.

---

#### **Usage**

##### Example Command
```bash
python evaluate_images.py --input-folder generated_images --output-folder benchmark_filtered --use-case "children's drawings" --threshold 7
```

##### Parameters
| Argument              | Description                                                                                                     | Required | Default             |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|----------|---------------------|
| `--input-folder`      | Path to the folder containing the images to evaluate.                                                           | Yes      | N/A                 |
| `--output-folder`     | Path to the folder where filtered images will be saved.                                                         | No       | `benchmark_filtered`|
| `--use-case`          | The style or use case to evaluate (e.g., "children's drawings," "vintage Polaroid").                            | Yes      | N/A                 |
| `--threshold`         | Minimum average score required for an image to pass the filter (scale of 1 to 10).                              | No       | 7                   |

---

#### **Workflow**
1. **Prepare Images**:
   - Place the images to be evaluated in the input folder.

2. **Run the Script**:
   - Specify the input folder, output folder, use case, and threshold.
   - The script will evaluate each image, calculate scores, and filter images based on the threshold.

3. **View Results**:
   - Images that pass the threshold will be saved in the output folder.

---

#### **Example Process**

For an image in the `generated_images` folder, if the `use-case` is "children's drawings," the script will:
1. Ask LLaVA questions like:
   - "On a scale from 1 to 10, how well does this image match the style of 'children's drawings'?"
   - "On a scale from 1 to 10, does this image have the typical visual characteristics of the specified style?"
   - "On a scale from 1 to 10, how likely is it that this image was designed with 'children's drawings' in mind?"
   - "On a scale from 1 to 10, how closely does this image's color palette match the intended style?"

2. Calculate an average score from the responses.

3. If the average score meets or exceeds the threshold (e.g., `7`), the image is saved in the output folder.

---

#### **Output**
- **Filtered Images**:
  - Images passing the threshold are saved to the specified output folder.
  - Images are not modified in the original folder.

- **Detailed Logs**:
  - Each image's evaluation process and scores are logged for debugging and transparency.


---

#### **Notes**
- Ensure your Replicate API key is set as an environment variable before running the script.
- Use the `--threshold` parameter to adjust the strictness of the filtering process.
- Review logs for any errors or unparsed model responses.

## **Feedback and Contributions**  
Have feedback or ideas to improve the scripts? Feel free to open an issue or submit a pull request!  

---


Enjoy building your benchmarks effortlessly! 🎉
