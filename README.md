# EasyPublicBackup 🚀  

### **Easily Backup Your public_html Folders Over SSH**  

## 📌 What is EasyPublicBackup?  
**EasyPublicBackup** is a simple tool that helps you **backup all public_html folders** from your server **over SSH** using `rsync`. It provides an **easy-to-use GUI** so you can **backup your website files with one click**.  

This tool is useful for:  
- **Developers** – Quickly copy website files.  
- **System Admins** – Automate backups.  
- **Hosting Users** – Securely save website data.  

No need for manual file transfers – just **connect, select, and backup!**  

---

## 🔧 How to Use  
### **1️⃣ Install Required Packages**  
Make sure you have Python and the required packages installed:  

```sh
pip install paramiko tkinter

 Download & Run

git clone https://github.com/your-username/EasyPublicBackup.git
cd EasyPublicBackup
python main_tk_app.py

3️⃣ Enter Your Server Details

    Host – Server IP or domain.
    Username – SSH login.
    Password – Required for authentication.
    Port – Default is 22.

4️⃣ Choose Your Backup Folder

Select where you want to save your backup files on your computer.
5️⃣ Select What to Download

    All Files – Backup everything.
    Without Images – Exclude .jpg, .jpeg, .png, .gif files.
    Only Images – Download only image files.

6️⃣ Click "Download" & Monitor Progress

    The app connects via SSH, finds public_html folders, and starts syncing files.
    The progress is shown in a table.
    Cancel anytime by clicking "Close".

📦 Requirements

    Python 3.8+
    paramiko (for SSH)
    rsync (for fast file syncing)
    tkinter (for GUI)

To install dependencies, run:

pip install -r requirements.txt

🌟 Features

✅ One-Click Backup – No complex commands needed.
✅ Secure SSH Connection – No unencrypted transfers.
✅ Custom Backup Location – Save backups anywhere.
✅ File Filtering – Choose what to download.
✅ Live Progress Tracking – See download status in real-time.
✅ Cancel Anytime – Stop ongoing downloads.
✅ Lightweight & Open-Source – Simple and free to use!
🛠️ Contributing

Want to help improve this project? Fork the repo, report issues, or submit pull requests!
📜 License

This project is licensed under the MIT License.
🔗 Links

🔹 GitHub Repository: [GitHub Repo Link]
🔹 Report Issues: [GitHub Issues Page]
🔹 Documentation: Coming soon!
