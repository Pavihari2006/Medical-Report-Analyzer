import re
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_findings(text):
    findings = []
    seen = set()
    patterns = [
        r"([A-Za-z][A-Za-z \-]{2,30}?)[:\-]\s*([\d.]+)\s*([a-zA-Z/%µμ]+)",
        r"([A-Za-z][A-Za-z \-]{2,30}?)\s+([\d.]+)\s*([a-zA-Z/%µμ]+)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            test_name, value, unit = match
            key = (test_name.strip().lower(), value.strip())
            if key in seen:
                continue
            seen.add(key)
            findings.append({
                "test_name": test_name.strip(),
                "value": value.strip(),
                "unit": unit.strip()
            })
    return findings


def explain_finding(test_name, value, unit):
    prompt = (
        f"Explain this medical test result in very simple language for a patient "
        f"with no medical background. Test: {test_name}, Value: {value} {unit}. "
        f"Keep it to 2-3 short sentences. Mention if it seems normal, high, or low "
        f"if you can tell, but do not give medical advice or diagnosis."
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                return "The AI explanation service is currently busy. Please try uploading this report again in a moment."
            return f"Could not generate explanation: {str(e)}"


if __name__ == "__main__":
    sample_text = "Hemoglobin: 10.2 g/dL"
    results = extract_findings(sample_text)
    for finding in results:
        explanation = explain_finding(finding["test_name"], finding["value"], finding["unit"])
        finding["simple_explanation"] = explanation
        print(finding)