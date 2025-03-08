import paramiko
import os
import threading
import tkinter as tk
from tkinter import ttk, Scrollbar, messagebox, filedialog
import subprocess

# Create a global stop event
stop_event = threading.Event()

def browse_directory():
    """Opens a dialog for the user to select the download folder."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        download_path.set(folder_selected)  # Update the path variable

def start_download():
    """Handles SSH connection and file download process."""
    global stop_event
    stop_event.clear()  # Reset stop event
    
    host = host_entry.get()
    user = user_entry.get()
    port = int(port_entry.get())
    password = password_entry.get()
    dest_dir = download_path.get()  # Get the user-selected directory
    
    if not dest_dir:
        messagebox.showwarning("Warning", "Please select a download directory.")
        return
    
    download_option = download_option_var.get()
    
    def connect_ssh():
        """Establish an SSH connection."""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=user, password=password)
            print("Connected successfully!")
            return client
        except Exception as e:
            messagebox.showerror("SSH Connection Failed", f"Failed to connect: {e}")
            return None

    def listHomeUser(client):
        """Lists valid home directories for users on the remote server."""
        exclude_dirs = {'lost+found', 'Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos',
                        '0_README_BEFORE_DELETING_VIRTFS', 'cagefs-skeleton', 'cldiaguser_cbc568c3c22540a5bc3f1',
                        'cPanelInstall', 'latest', 'my.cnf', 'virtfs'}
        try:
            stdin, stdout, stderr = client.exec_command("ls /home")
            all_dirs = stdout.read().decode().split()
            return [d for d in all_dirs if d not in exclude_dirs]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list directories: {e}")
            return []

    def downloadFolderWithRsync(source_dir, index):
        """Uses rsync to download folders from the remote server."""
        if stop_event.is_set():
            folder_table.item(index, values=(index + 1, os.path.basename(source_dir.rstrip('/')), "Cancelled"))
            return

        try:
            folder_name = os.path.basename(source_dir.rstrip('/'))
            if folder_name == 'backup_CAT_KILLER_NUPI_SIBIDI':
                folder_table.item(index, values=(index + 1, folder_name, "Skipped"))
                return
            
            target_dir = os.path.join(dest_dir, folder_name)
            os.makedirs(target_dir, exist_ok=True)
            
            exclude_option = ""
            if download_option == "Without Images":
                exclude_option = "--exclude='*.jpg' --exclude='*.jpeg' --exclude='*.png' --exclude='*.gif'"
            elif download_option == "Only Images":
                exclude_option = "--include='*.jpg' --include='*.jpeg' --include='*.png' --include='*.gif' --exclude='*'"
            
            rsync_command = f"sshpass -p '{password}' rsync -avz -e 'ssh -p {port}' {exclude_option} {user}@{host}:{source_dir}/ {target_dir}/"

            folder_table.item(index, values=(index + 1, folder_name, "In Progress"))
            root.update_idletasks()
            
            process = subprocess.Popen(rsync_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            while process.poll() is None:
                if stop_event.is_set():
                    process.terminate()
                    folder_table.item(index, values=(index + 1, folder_name, "Cancelled"))
                    return

            if process.returncode == 0:
                folder_table.item(index, values=(index + 1, folder_name, "Completed"))
            else:
                folder_table.item(index, values=(index + 1, folder_name, "Failed"))

        except Exception as e:
            folder_table.item(index, values=(index + 1, folder_name, "Failed"))
            messagebox.showerror("Download Error", f"Failed to download {folder_name}: {e}")

    client = connect_ssh()
    if not client:
        return
    
    listUserDirs = listHomeUser(client)
    if not listUserDirs:
        client.close()
        return
    
    folders_to_download = []
    for userDir in listUserDirs:
        public_html_path = f"/home/{userDir}/public_html"
        stdin, stdout, stderr = client.exec_command(f"ls -Ad {public_html_path}/*/")
        list_dirs_public_html_path = stdout.read().decode().split()
        
        for list_dirs in list_dirs_public_html_path:
            folders_to_download.append(list_dirs.rstrip('/'))
    
    client.close()
    
    for index, folder in enumerate(folders_to_download):
        folder_table.insert("", "end", iid=index, values=(index + 1, os.path.basename(folder), "Pending"))

    def start_download_thread():
        for index, folder in enumerate(folders_to_download):
            if stop_event.is_set():
                break
            downloadFolderWithRsync(folder, index)

    threading.Thread(target=start_download_thread, daemon=True).start()

def close_application():
    """Stops the ongoing downloads and closes the application."""
    stop_event.set()
    root.quit()

root = tk.Tk()
root.title("SSH File Downloader")
root.geometry("1024x650")

download_path = tk.StringVar(value="./backup")  

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Host:").grid(row=0, column=0, sticky="w")
host_entry = tk.Entry(frame, width=30)
host_entry.grid(row=0, column=1)

tk.Label(frame, text="Username:").grid(row=1, column=0, sticky="w")
user_entry = tk.Entry(frame, width=30)
user_entry.grid(row=1, column=1)

tk.Label(frame, text="Port:").grid(row=2, column=0, sticky="w")
port_entry = tk.Entry(frame, width=30)
port_entry.insert(0, "22")
port_entry.grid(row=2, column=1)

tk.Label(frame, text="Password:").grid(row=3, column=0, sticky="w")
password_entry = tk.Entry(frame, width=30, show="*")
password_entry.grid(row=3, column=1)

tk.Label(frame, text="Download Path:").grid(row=4, column=0, sticky="w")
path_entry = tk.Entry(frame, textvariable=download_path, width=30)
path_entry.grid(row=4, column=1)
tk.Button(frame, text="Browse", command=browse_directory).grid(row=4, column=2)

download_option_var = tk.StringVar(value="Without Images")

tk.Label(frame, text="Download Options:").grid(row=5, column=0, sticky="w")
tk.Radiobutton(frame, text="Without Images", variable=download_option_var, value="Without Images").grid(row=5, column=1, sticky="w")
tk.Radiobutton(frame, text="With Images", variable=download_option_var, value="With Images").grid(row=6, column=1, sticky="w")
tk.Radiobutton(frame, text="Only Images", variable=download_option_var, value="Only Images").grid(row=7, column=1, sticky="w")

tk.Button(frame, text="Download", command=start_download).grid(row=8, columnspan=3, pady=10)

tk.Button(root, text="Close", command=close_application).pack(pady=10)

folder_frame = tk.Frame(root, padx=20, pady=20)
folder_frame.pack(fill="both", expand=True)

tk.Label(folder_frame, text="Download Progress").pack()
folder_table = ttk.Treeview(folder_frame, columns=("SRNO", "FOLDER NAME", "STATUS"), show="headings")
folder_table.heading("SRNO", text="SRNO")
folder_table.heading("FOLDER NAME", text="FOLDER NAME")
folder_table.heading("STATUS", text="STATUS")
folder_table.pack(fill="both", expand=True)

root.mainloop()
