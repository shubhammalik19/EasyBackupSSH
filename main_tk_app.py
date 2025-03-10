import paramiko
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Create a global stop event
stop_event = threading.Event()

def browse_directory():
    """Opens a dialog for the user to select the download folder."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        download_path.set(folder_selected)  # Update the path variable

def start_download():
    """Handles SSH connection and file download process."""
    stop_event.clear()  # Reset stop event
    progress["value"] = 0  # Reset progress bar

    host = host_entry.get()
    user = user_entry.get()
    port = int(port_entry.get())
    password = password_entry.get()
    dest_dir = download_path.get()  # Get the user-selected directory

    if not dest_dir:
        messagebox.showwarning("Warning", "Please select a download directory.")
        return

    def connect_ssh():
        """Establish an SSH connection."""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=user, password=password)
            return client
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("SSH Connection Failed", f"Failed to connect: {e}"))
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
            root.after(0, lambda: messagebox.showerror("Error", f"Failed to list directories: {e}"))
            return []

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

    if len(folders_to_download) > 0:
        progress_step = 100 / len(folders_to_download)
    else:
        progress_step = 100  

    for index, folder in enumerate(folders_to_download):
        folder_table.insert("", "end", iid=index, values=(index + 1, os.path.basename(folder), "Pending"))

    def downloadFolderWithRsync(source_dir, index):
        """Uses rsync to download folders from the remote server."""
        if stop_event.is_set():
            root.after(0, lambda: folder_table.item(index, values=(index + 1, os.path.basename(source_dir.rstrip('/')), "Cancelled")))
            return

        try:
            folder_name = os.path.basename(source_dir.rstrip('/'))
            if folder_name == 'backup_CAT_KILLER_NUPI_SIBIDI':
                root.after(0, lambda: folder_table.item(index, values=(index + 1, folder_name, "Skipped")))
                return
            
            target_dir = os.path.join(dest_dir, folder_name)
            os.makedirs(target_dir, exist_ok=True)

            exclude_option = "--exclude='node_modules' --exclude='vendor' --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.png' --exclude='*.gif'"

            root.after(0, lambda: folder_table.item(index, values=(index + 1, folder_name, "In Progress")))

            rsync_command = f"sshpass -p '{password}' rsync -avz -e 'ssh -p {port}' {exclude_option} {user}@{host}:{source_dir}/ {target_dir}/"

            process = subprocess.Popen(rsync_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            while process.poll() is None:
                if stop_event.is_set():
                    process.terminate()
                    root.after(0, lambda: folder_table.item(index, values=(index + 1, folder_name, "Cancelled")))
                    return

            if process.returncode == 0:
                root.after(0, lambda: folder_table.item(index, values=(index + 1, folder_name, "Completed")))
            else:
                root.after(0, lambda: folder_table.item(index, values=(index + 1, folder_name, "Failed")))

            root.after(0, lambda: update_progress(progress["value"] + progress_step))

        except Exception as e:
            root.after(0, lambda: folder_table.item(index, values=(index + 1, folder_name, "Failed")))
            root.after(0, lambda: messagebox.showerror("Download Error", f"Failed to download {folder_name}: {e}"))

    def start_download_thread():
        with ThreadPoolExecutor(max_workers=4) as executor:
            [executor.submit(downloadFolderWithRsync, folder, index) for index, folder in enumerate(folders_to_download)]

        root.after(0, lambda: progress.config(value=100))

    threading.Thread(target=start_download_thread, daemon=True).start()

def close_application():
    """Stops all ongoing downloads and properly closes the application."""
    stop_event.set()  # Signal all threads to stop

    # Find and terminate any running rsync processes
    try:
        subprocess.run("pkill -f rsync", shell=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error stopping rsync: {e}")

    root.quit()  # Stop the Tkinter main event loop
    root.destroy()  # Destroy all UI components and exit completely

def update_progress(value):
    progress["value"] = value
    root.after(100, lambda: progress.update_idletasks())

def browse_directory():
    """Opens a dialog for the user to select the download folder."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        download_path.set(folder_selected)  # Update the path variable


# GUI Setup
root = tk.Tk()
root.title("SSH File Downloader")
root.geometry("1024x650")

download_path = tk.StringVar(value="/home/shubham/ssh_python/backup")
host = tk.StringVar(value="logisticsoftware.in")
user = tk.StringVar(value="root")
port = tk.StringVar(value="8165")
password = tk.StringVar(value="your_password")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Host:").grid(row=0, column=0, sticky="w")
host_entry = tk.Entry(frame, width=30, textvariable=host)
host_entry.grid(row=0, column=1)

tk.Label(frame, text="Username:").grid(row=1, column=0, sticky="w")
user_entry = tk.Entry(frame, width=30, textvariable=user)
user_entry.grid(row=1, column=1)

tk.Label(frame, text="Port:").grid(row=2, column=0, sticky="w")
port_entry = tk.Entry(frame, width=30, textvariable=port)
port_entry.grid(row=2, column=1)

tk.Label(frame, text="Password:").grid(row=3, column=0, sticky="w")
password_entry = tk.Entry(frame, width=30, show="*", textvariable=password)
password_entry.grid(row=3, column=1)

tk.Label(frame, text="Backup Path:").grid(row=4, column=0, sticky="w")
path_entry = tk.Entry(frame, width=30, textvariable=download_path)
path_entry.grid(row=4, column=1)
tk.Button(frame, text="Browse", command=browse_directory).grid(row=4, column=2, padx=5)


progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress.pack(pady=10)

tk.Button(frame, text="Download", command=start_download).grid(row=8, columnspan=3, pady=10)
tk.Button(root, text="Close", command=close_application).pack(pady=10)

folder_frame = tk.Frame(root, padx=20, pady=20)
folder_frame.pack(fill="both", expand=True)

folder_table = ttk.Treeview(folder_frame, columns=("SRNO", "FOLDER NAME", "STATUS"), show="headings")
folder_table.pack(fill="both", expand=True)

root.mainloop()
