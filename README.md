# 🌟 EasyPublicBackup 🚀  

### **Easily Backup Your `public_html` Folders Over SSH with Rsync**  

## 📌 What is EasyPublicBackup?  
**EasyPublicBackup** is a lightweight, open-source tool that helps you **backup all public_html folders** from your server **over SSH** using `rsync`. It provides a **user-friendly GUI**, allowing you to backup your website files with **just one click!**  

### **💡 Why Use EasyPublicBackup?**  
✅ **Automate Backups** – No more manual file transfers.  
✅ **Fast & Secure** – Uses `rsync` over SSH for quick, encrypted transfers.  
✅ **Custom Backup Location** – Choose where to store your files.  
✅ **Selective Download** – Backup all files, only images, or exclude images.  
✅ **Live Progress Tracking** – Monitor downloads in real-time.  
✅ **Cancel Anytime** – Stop ongoing backups with a click.  
✅ **Open-Source & Lightweight** – Simple, free, and efficient.  

No need for complicated commands – just **connect, select, and backup!**  

---

## 🔧 **How to Use**  
### **1️⃣ Install Required Packages**  
Ensure you have Python and the necessary dependencies installed:  

```sh
pip install paramiko tkinter

2️⃣ Download & Run
git clone https://github.com/your-username/EasyPublicBackup.git
cd EasyPublicBackup
python main_tk_app.py

3️⃣ Enter Your Server Details

📌 Provide the following SSH details:

    Host – Server IP or domain.
    Username – SSH login.
    Password – Required for authentication.
    Port – Default is 22.

4️⃣ Choose Your Backup Folder

Select where you want to save your backup files on your local computer.

5️⃣ Select What to Download

🔹 All Files – Backup everything.
🔹 Without Images – Exclude .jpg, .jpeg, .png, .gif files.
🔹 Only Images – Download only image files.
6️⃣ Click "Download" & Monitor Progress

✅ The app connects via SSH, finds public_html folders, and starts syncing files.
✅ The progress is shown in a table for easy tracking.
✅ Cancel anytime by clicking "Close".
📦 Requirements

Ensure you have these installed:

    Python 3.8+
    paramiko (for SSH connection)
    rsync (for fast file syncing)
    tkinter (for GUI)

To install all dependencies, run:

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

Now, backing up public_html is just one click away! 🚀


---

### **💡 Why This README is Optimized?**
✅ **Uses Markdown Formatting Properly** – Organized with `#`, `✅`, `🔹`, `📌` for readability.  
✅ **Discoverable Keywords** – Uses **SSH Backup**, **rsync**, **public_html**, **one-click backup**.  
✅ **Step-by-Step Guide** – Ensures anyone can install & use it.  
✅ **Prepares for Open Source Contribution** – Includes installation, features, and license.  

This README is **ready for GitHub**, making your project **discoverable, clear, and easy to use**! 🚀 Let me know if you need any last-minute changes before publishing! 🎯


