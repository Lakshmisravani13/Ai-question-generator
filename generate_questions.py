import json
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

# Load model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base").to("cpu")  # Use "cuda" if GPU available

# Load your extracted JSON
with open("extracted_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Store generated questions
generated_questions = []

# Process each image
for page in data:
    for img_path in page["images"]:
        image = Image.open(img_path).convert("RGB")

        question_prompt = "What is shown in the image?"
        inputs = processor(image, question_prompt, return_tensors="pt").to("cpu")
        out = model.generate(**inputs)
        answer = processor.decode(out[0], skip_special_tokens=True)

        generated_questions.append({
            "image": img_path,
            "generated_question": question_prompt,
            "predicted_answer": answer
        })

# Save to file
with open("generated_questions.json", "w", encoding="utf-8") as f:
    json.dump(generated_questions, f, indent=2)

print("✅ AI-generated questions saved to generated_questions.json")
