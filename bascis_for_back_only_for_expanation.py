import paramiko
import os
import sys

# Define connection parameters
host = "logisticsoftware.in"
user = "root"
port = 8165
password = "wR##5Tu#s11E"  # Replace with the actual password

def connect_ssh():
    """Connects to the SSH server using paramiko."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=user, password=password)
        print("Connected successfully!")
        return client
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def listHomeUser(client):
    """Lists the all the directories in the home directory of the user excluding some which is not relevant"""
    exclude_dirs = {'lost+found', 'Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos',
                    '0_README_BEFORE_DELETING_VIRTFS', 'cagefs-skeleton', 'cldiaguser_cbc568c3c22540a5bc3f1',
                    'cPanelInstall', 'latest', 'my.cnf', 'virtfs'}
    try:
    y    stdin, stdout, stderr = client.exec_command("ls /home")
        all_dirs = stdout.read().decode().split()
        filtered_dirs = [d for d in all_dirs if d not in exclude_dirs]
        print("Filtered directories in home directory:")
        for d in filtered_dirs:
            print(d)
        return filtered_dirs
    except Exception as e:
        print(f"Failed to list directories: {e}")
        return []

def downloadFolderWithRsync(source_dir, dest_dir, is_image_excluded=False):
    """Downloads a folder using rsync with sshpass from the server to the local machine"""
    try:
        dir_name_sorce = os.path.basename(source_dir.rstrip('/'))
        #print(dir_name_sorce)
        
        dest_dir = os.path.join(dest_dir, dir_name_sorce)
        #print(f"Destination directory: {dest_dir}")
        #sys.exit(0)
        exclude_option = "--exclude='*.jpg' --exclude='*.jpeg' --exclude='*.png' --exclude='*.gif'" if is_image_excluded else ""
        rsync_command = f"sshpass -p '{password}' rsync -avz -e 'ssh -p {port}' {exclude_option} {user}@{host}:{source_dir} {dest_dir} > /dev/null 2>&1"
        #print(f"Executing: {rsync_command}")
        os.system(rsync_command)
        #sys.exit(0)
        print("Download completed successfully.")
    except Exception as e:
        print(f"Failed to download folder: {e}")

if __name__ == "__main__":
    client = connect_ssh()
    if not client:
        sys.exit(1)

    listUserDirs = listHomeUser(client)
    if not listUserDirs:
        print("No directories found or an error occurred.")
        client.close()
        sys.exit(1)
    
    for userDir in listUserDirs:
        print(f"Checking directory: {userDir}")
        if userDir == "cagefs-skeleton":
            print(f"Skipping {userDir} as it is not a valid directory.")
            continue
        
        public_html_path = f"/home/{userDir}/public_html"
        stdin, stdout, stderr = client.exec_command(f"ls -Ad {public_html_path}/*/")
        list_dirs_public_html_path = stdout.read().decode().split()
        
        if not list_dirs_public_html_path:
            print(f"The directory /home/{userDir} is empty.")
            continue
        
        for list_dirs in list_dirs_public_html_path:
            #print(f"Checking directory: {list_dirs}")
            local_backup_path = "/home/shubham/ssh_python/backup"
            downloadFolderWithRsync(list_dirs, local_backup_path)
    
    client.close()
