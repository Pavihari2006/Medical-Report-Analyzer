def clean_text(text: String) -> String:
    var words = text.split()
    var result = String(" ").join(words)
    return result

def main() raises:
    var input_text: String = ""
    with open("input.txt", "r") as f:
        input_text = f.read()
    var cleaned = clean_text(input_text)
    with open("output.txt", "w") as f:
        f.write(cleaned)
    print(cleaned)