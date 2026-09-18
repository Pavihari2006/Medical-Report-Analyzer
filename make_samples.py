from PIL import Image, ImageDraw

samples = [
    "Hemoglobin: 10.2 g/dL",
    "Blood Sugar: 145 mg/dL",
    "Cholesterol - 220 mg/dL",
    "WBC Count: 11200 cells/mcL",
    "Platelet Count: 180000 /mcL",
    "Vitamin D: 18 ng/mL",
    "Creatinine: 1.4 mg/dL",
    "TSH: 5.8 mIU/L",
    "Blood Pressure: 140 mmHg",
    "HbA1c: 7.2 %",
]

for i, text in enumerate(samples, start=1):
    img = Image.new('RGB', (500, 100), color='white')
    d = ImageDraw.Draw(img)
    d.text((10, 40), text, fill='black')
    filename = f"sample{i}.png"
    img.save(filename)
    print(f"Created {filename}: {text}")