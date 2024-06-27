import os
import re
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
import PyPDF2
import difflib


import os
import re
from docx import Document
import PyPDF2

import os
import re
from docx import Document
from PyPDF2 import PdfReader  # Import PdfReader from PyPDF2

def read_file(file_path):
    """ Read and return the contents of a file based on its type (PDF, DOCX, TXT). """
    _, file_extension = os.path.splitext(file_path.lower())
    file_extension = file_extension[1:]  # Remove the dot from the extension

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
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text.append(page.extract_text())
            return '\n'.join(text)
    else:
        return ''  # Handle unsupported file types or return an empty string

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

    # Sort results by similarity in descending order
    results.sort(key=lambda x: x[1], reverse=True)
    return results
