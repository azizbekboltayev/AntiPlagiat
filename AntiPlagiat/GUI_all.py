import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core_all import compare_files

# Function to handle selecting a target file
def select_target_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        target_file_path.set(file_path)

# Function to handle selecting a folder
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)

# Function to run the comparison and update the table
def run_comparison():
    target_file = target_file_path.get()
    folder = folder_path_var.get()
    if not target_file or not folder:
        messagebox.showerror("Error", "Please select both the target file and the folder.")
        return

    results = compare_files(target_file, folder)
    update_table(results)

# Function to update the table with comparison results
def update_table(results):
    # Clear previous results
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Create headers
    ctk.CTkLabel(table_frame, text="Filename", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
    ctk.CTkLabel(table_frame, text="Similarity (%)", font=("Helvetica", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)

    # Display results
    max_similarity = max(result[1] for result in results) if results else 1.0  # Avoid division by zero
    for index, (filename, similarity) in enumerate(results, start=1):
        # Calculate font size based on similarity percentage
        font_size = int(12 + 6 * (similarity / max_similarity))  # Adjust the multiplier for font size scaling
        font = ("Helvetica", font_size)
        
        ctk.CTkLabel(table_frame, text=filename, font=font).grid(row=index, column=0, padx=10, pady=5)
        ctk.CTkLabel(table_frame, text=f"{similarity:.2f}", font=font).grid(row=index, column=1, padx=10, pady=5)

# Create the main window
root = ctk.CTk()
root.title("Anti-Plagiarism Tool")
root.geometry("800x600")

# Variables to store the selected file and folder paths
target_file_path = tk.StringVar()
folder_path_var = tk.StringVar()

# Create and place widgets
header = ctk.CTkLabel(root, text="Anti-Plagiarism Tool", font=("Helvetica", 24, "bold"))
header.pack(pady=20)

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Target File:", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
ctk.CTkEntry(frame, textvariable=target_file_path, width=400, font=("Helvetica", 14)).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(frame, text="Browse", command=select_target_file).grid(row=0, column=2, padx=10, pady=10)

ctk.CTkLabel(frame, text="Folder:", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
ctk.CTkEntry(frame, textvariable=folder_path_var, width=400, font=("Helvetica", 14)).grid(row=1, column=1, padx=10, pady=10)
ctk.CTkButton(frame, text="Browse", command=select_folder).grid(row=1, column=2, padx=10, pady=10)

ctk.CTkButton(frame, text="Run Comparison", command=run_comparison, fg_color="#4CAF50", hover_color="#45A049", font=("Helvetica", 16)).grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Create a frame for the table
table_frame = ctk.CTkFrame(root)
table_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Start the main loop
root.mainloop()
