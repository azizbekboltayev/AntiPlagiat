import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core_all import compare_files  

def select_target_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        target_file_path.set(file_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)

def run_comparison():
    target_file = target_file_path.get()
    folder = folder_path_var.get()
    if not target_file or not folder:
        messagebox.showerror("Error", "Please select both the target file and the folder.")
        return

    progress_bar.set(0)
    progress_label.configure(text="Starting...")

    root.update_idletasks()

    results = compare_files(target_file, folder, progress_callback)
    update_table(results)

    progress_label.configure(text="Comparison complete.")
    progress_bar.set(100)

def progress_callback(current, total, filename):
    progress_percentage = (current / total) * 100
    progress_bar.set(progress_percentage)
    progress_label.configure(text=f"Processing: {filename} ({progress_percentage:.2f}%)")
    root.update_idletasks()

def update_table(results):
    for widget in result_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(result_frame, text="Filename", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
    ctk.CTkLabel(result_frame, text="Similarity (%)", font=("Helvetica", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)

    max_similarity = max(result[1] for result in results) if results else 1.0
    for index, (filename, similarity) in enumerate(results, start=1):
        font_size = int(12 + 6 * (similarity / max_similarity))
        font = ("Helvetica", font_size)
        
        ctk.CTkLabel(result_frame, text=filename, font=font).grid(row=index, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(result_frame, text=f"{similarity:.2f}", font=font).grid(row=index, column=1, padx=10, pady=5, sticky="w")

root = ctk.CTk()
root.title("Anti-Plagiarism Tool")
root.geometry("800x600")

target_file_path = tk.StringVar()
folder_path_var = tk.StringVar()

header = ctk.CTkLabel(root, text="Anti-Plagiarism Tool", font=("Helvetica", 24, "bold"))
header.grid(row=0, column=0, columnspan=3, pady=20)

frame = ctk.CTkFrame(root)
frame.grid(row=1, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")

ctk.CTkLabel(frame, text="Target File:", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
ctk.CTkEntry(frame, textvariable=target_file_path, width=400, font=("Helvetica", 14)).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkButton(frame, text="Browse", command=select_target_file).grid(row=0, column=2, padx=10, pady=10, sticky="w")

ctk.CTkLabel(frame, text="Folder:", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
ctk.CTkEntry(frame, textvariable=folder_path_var, width=400, font=("Helvetica", 14)).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkButton(frame, text="Browse", command=select_folder).grid(row=1, column=2, padx=10, pady=10, sticky="w")

ctk.CTkButton(frame, text="Run Comparison", command=run_comparison, fg_color="#4CAF50", hover_color="#45A049", font=("Helvetica", 16)).grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

progress_bar = ctk.CTkProgressBar(root, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, pady=10, padx=20, sticky="ew")
progress_bar.set(0)  

progress_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))
progress_label.grid(row=4, column=0, columnspan=3, pady=5)

result_frame = ctk.CTkFrame(root)
result_frame.grid(row=5, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")


root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

root.update_idletasks()

root.mainloop()