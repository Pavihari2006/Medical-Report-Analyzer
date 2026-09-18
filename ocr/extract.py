import pytesseract
from PIL import Image
import subprocess
import os
 
MOJO_DIR = os.path.join(os.path.dirname(__file__), "..", "mojo")
 
 
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
 
 
def clean_text_with_mojo(text):
    try:
        input_path = os.path.join(MOJO_DIR, "input.txt")
        output_path = os.path.join(MOJO_DIR, "output.txt")
 
        with open(input_path, "w") as f:
            f.write(text)
 
        subprocess.run(
            ["pixi", "run", "mojo", "run", "clean_text.mojo"],
            cwd=MOJO_DIR,
            capture_output=True, text=True, timeout=30
        )
 
        with open(output_path, "r") as f:
            cleaned = f.read()
        return cleaned.strip()
    except Exception:
        return text
 
 
if __name__ == "__main__":
    result = extract_text_from_image("../sample.png")
    print("Raw OCR:", result)
    cleaned = clean_text_with_mojo(result)
    print("Mojo Cleaned:", cleaned)
 