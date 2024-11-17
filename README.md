# Gen-AI-Benchmark-Automation

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
Clone this repository and ensure the necessary dependencies are installed.  

```bash
git clone https://github.com/your-repo-name.git  
cd your-repo-name  
pip install -r requirements.txt  
```

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
- `manual_review.py`: Assists with the final manual curation process.  
- `requirements.txt`: Lists all required Python dependencies.  
- `README.md`: Documentation for this repository.  

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

## **Feedback and Contributions**  
Have feedback or ideas to improve the scripts? Feel free to open an issue or submit a pull request!  

---

## **License**  
This repository is open-source under the [MIT License](LICENSE).  

Enjoy building your benchmarks effortlessly! 🎉
