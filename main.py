import os
import json
import pdfplumber
import fitz  # pymupdf

# Path to your PDF file
pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"

# Create output folder for images
output_image_folder = "extracted_images"
os.makedirs(output_image_folder, exist_ok=True)

# Step 1: Extract Text using pdfplumber
text_by_page = []
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        text_by_page.append({"page": i + 1, "text": text})

# Step 2: Extract Images using PyMuPDF
doc = fitz.open(pdf_path)
image_output = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    images = page.get_images(full=True)
    image_paths = []

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"{output_image_folder}/page{page_num+1}_image{img_index+1}.{image_ext}"
        with open(image_filename, "wb") as img_file:
            img_file.write(image_bytes)
        image_paths.append(image_filename)

    image_output.append({"page": page_num + 1, "images": image_paths})

# Step 3: Combine Text and Image Paths into JSON
combined_output = []
for i in range(len(text_by_page)):
    combined_output.append({
        "page": i + 1,
        "text": text_by_page[i]["text"],
        "images": image_output[i]["images"] if i < len(image_output) else []
    })

# Save to JSON file
with open("extracted_data.json", "w", encoding="utf-8") as f:
    json.dump(combined_output, f, indent=2, ensure_ascii=False)

print("✅ Done! Text and images extracted successfully.")
