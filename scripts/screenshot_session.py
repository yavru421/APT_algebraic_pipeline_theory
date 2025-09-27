"""
APT Screenshot Session Capture & Analysis
- Captures screenshots every X seconds while user performs a task
- After session, runs APT screenshot pipeline on all captured images
- Aggregates and visualizes UI evolution as a dynamic graph
"""
import os
import time
import glob
import subprocess
from datetime import datetime

def capture_screenshot(out_dir, prefix):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = os.path.join(out_dir, f"{prefix}_{timestamp}.png")
    # Windows screenshot using PowerShell
    cmd = f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen(0, 0, 0, 0, $bmp.Size); $bmp.Save('{out_path}'); $graphics.Dispose(); $bmp.Dispose()\""
    subprocess.run(cmd, shell=True)
    print(f"Captured screenshot: {out_path}")
    return out_path

def run_apt_pipeline_on_dir(img_dir):
    # Run the APT screenshot pipeline on all images in img_dir
    import shutil
    pipeline = os.path.join(os.path.dirname(__file__), "pipeline.py")
    results_dir = os.path.join(img_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    imgs = glob.glob(os.path.join(img_dir, '*.png'))
    for img in imgs:
        # Move/copy to examples/ for pipeline
        shutil.copy(img, os.path.join(os.path.dirname(pipeline), "examples", os.path.basename(img)))
    # Run pipeline
    os.chdir(os.path.dirname(pipeline))
    os.system("python pipeline.py")
    print("APT screenshot pipeline complete.")

def main():
    session_dir = os.path.join("..", "apt_image_pipeline", "screenshots")
    os.makedirs(session_dir, exist_ok=True)
    try:
        interval = float(input("Enter screenshot interval in seconds (e.g., 10): "))
    except Exception:
        interval = 10.0
    duration = 60.0  # Default to 1 minute
    print(f"Session duration set to {duration} seconds (1 minute) by default.")
    prefix = "session"
    n_shots = int(duration // interval)
    print(f"Capturing {n_shots} screenshots every {interval} seconds...")
    for i in range(n_shots):
        capture_screenshot(session_dir, prefix)
        if i < n_shots - 1:
            time.sleep(interval)
    print("Session capture complete. Running APT pipeline...")
    run_apt_pipeline_on_dir(session_dir)
    print("Session analysis complete.")

if __name__ == "__main__":
    main()
