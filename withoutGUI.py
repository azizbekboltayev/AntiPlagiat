import os
import difflib
import re

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def normalize_text(text):
    # Remove punctuation and normalize whitespace
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_similarity(file1_content, file2_content):
    sequence_matcher = difflib.SequenceMatcher(None, file1_content, file2_content)
    return sequence_matcher.ratio() * 100

def compare_files(target_file_path, folder_path):
    target_content = read_file(target_file_path)
    target_content = normalize_text(target_content)
    results = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_content = read_file(file_path)
            file_content = normalize_text(file_content)
            similarity = calculate_similarity(target_content, file_content)
            results.append((filename, similarity))

    return results

def main(target_file_path, folder_path):
    similarities = compare_files(target_file_path, folder_path)
    for filename, similarity in similarities:
        print(f"{filename}: {similarity:.2f}% similar")

if __name__ == "__main__":
    target_file_path = input("Enter the path to the specific file: ")
    folder_path = input("Enter the path to the folder: ")
    main(target_file_path, folder_path)
