import os
import re
from docx import Document
from PyPDF2 import PdfReader
import difflib
from concurrent.futures import ThreadPoolExecutor

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path.lower())
    file_extension = file_extension[1:]

    if file_extension == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_extension == 'docx':
        doc = Document(file_path)
        return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    elif file_extension == 'pdf':
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            return '\n'.join(text)
    else:
        return ''

def normalize_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_similarity(file1_content, file2_content):
    sequence_matcher = difflib.SequenceMatcher(None, file1_content, file2_content)
    return sequence_matcher.ratio() * 100

def process_file(file_path, target_content):
    file_content = read_file(file_path)
    file_content = normalize_text(file_content)
    similarity = calculate_similarity(target_content, file_content)
    return file_path, similarity

def compare_files(target_file_path, folder_path, progress_callback=None):
    target_content = read_file(target_file_path)
    target_content = normalize_text(target_content)
    results = []

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, filename in enumerate(files):
            file_path = os.path.join(folder_path, filename)
            futures.append(executor.submit(process_file, file_path, target_content))

        for i, future in enumerate(futures):
            result = future.result()
            results.append(result)
            if progress_callback:
                progress_callback(i + 1, total_files, result[0])

    results.sort(key=lambda x: x[1], reverse=True)
    return results
