import os
import difflib
import re

def read_file(file_path):
    """ Read and return the contents of a file. """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def normalize_text(text):
    """ Normalize text for comparison by removing punctuation and extra spaces, and converting to lowercase. """
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_similarity(file1_content, file2_content):
    """ Calculate and return similarity percentage between two texts. """
    sequence_matcher = difflib.SequenceMatcher(None, file1_content, file2_content)
    return sequence_matcher.ratio() * 100

def compare_files(target_file_path, folder_path):
    """ Compare the target file with all files in a folder and return a list of (filename, similarity) tuples. """
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

    results.sort(key=lambda x: x[1], reverse=True)
    return results
