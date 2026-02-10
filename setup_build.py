import os
import sys
import subprocess
import shutil

# --- Configuration ---
APP_NAME = "BenameurEditeur_Pro"
MAIN_FILE = "benameur_editeur_v3_7.py"
ICON_PATH = os.path.join("assets", "logo.ico")

def get_customtkinter_path():
    import customtkinter
    return os.path.dirname(customtkinter.__file__)

def build():
    print(f"--- Starting Build Process for {APP_NAME} ---")
    
    ctk_path = get_customtkinter_path()
    print(f"Found customtkinter at: {ctk_path}")
    
    # PyInstaller Command Construction
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--name={APP_NAME}",
        f"--add-data={ctk_path}{os.pathsep}customtkinter",
        f"--add-data=assets{os.pathsep}assets",
        MAIN_FILE
    ]
    
    if ICON_PATH and os.path.exists(ICON_PATH):
        cmd.insert(3, f"--icon={ICON_PATH}")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n[SUCCESS] Build completed. Check the 'dist' folder for your executable.")
    except Exception as e:
        print(f"\n[ERROR] Build failed: {e}")

if __name__ == "__main__":
    # Ensure pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    build()
