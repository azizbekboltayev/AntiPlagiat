import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core_all import compare_files
import threading

# Global variables for thread control
pause_event = threading.Event()
comparison_thread = None  # Global variable to hold the comparison thread

def select_target_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        target_file_path.set(file_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)

def clear_results():
    result_listbox.delete(0, tk.END)

def run_comparison_thread():
    global comparison_thread, pause_event

    clear_results()  # Clear previous results

    target_file = target_file_path.get()
    folder = folder_path_var.get()
    if not target_file or not folder:
        messagebox.showerror("Error", "Please select both the target file and the folder.")
        return
    
    run_comparison_button.configure(state=tk.DISABLED)
    pause_button.configure(state=tk.NORMAL)

    progress_bar.set(0)
    progress_label.configure(text="Starting...")

    # Reset events
    pause_event.clear()

    global comparison_thread
    comparison_thread = threading.Thread(target=run_comparison, args=(target_file, folder))
    comparison_thread.start()

def run_comparison(target_file, folder):
    results = compare_files(target_file, folder, progress_callback, pause_event)
    update_table(results)

    run_comparison_button.configure(state=tk.NORMAL)
    pause_button.configure(state=tk.DISABLED)

    progress_label.configure(text="Comparison complete.")
    progress_bar.set(100)

def progress_callback(current, total, filename):
    progress_percentage = (current / total) * 100
    progress_bar.set(progress_percentage)
    progress_label.configure(text=f"Processing: {filename} ({progress_percentage:.2f}%)")
    root.update_idletasks()

def update_table(results):
    result_listbox.delete(0, tk.END)

    for filename, similarity in results:
        result_listbox.insert(tk.END, f"{filename}: {similarity:.2f}%")

def pause_resume_comparison():
    if pause_button.cget("text") == "Pause":
        pause_event.set()
        pause_button.configure(text="Resume")
    else:
        pause_event.clear()
        pause_button.configure(text="Pause")

# GUI setup
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

run_comparison_button = ctk.CTkButton(frame, text="Run Comparison", command=run_comparison_thread, fg_color="#4CAF50", hover_color="#45A049", font=("Helvetica", 16))
run_comparison_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

pause_button = ctk.CTkButton(frame, text="Pause", command=pause_resume_comparison, fg_color="#FFC107", hover_color="#FFB300", font=("Helvetica", 16))
pause_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
pause_button.configure(state=tk.DISABLED)

progress_bar = ctk.CTkProgressBar(root, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=3, pady=10, padx=20, sticky="ew")
progress_bar.set(0)

progress_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))
progress_label.grid(row=5, column=0, columnspan=3, pady=5)

result_frame = ctk.CTkFrame(root)
result_frame.grid(row=6, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")

# Set the background color for the Listbox
listbox_bg_color = "#333333"  # Example color, adjust to match your app's background color
listbox_fg_color = "#FFFFFF"  # Example color, adjust to match your app's text color

result_listbox = tk.Listbox(result_frame, font=("Helvetica", 14), bg=listbox_bg_color, fg=listbox_fg_color)
result_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

root.update_idletasks()

root.mainloop()
