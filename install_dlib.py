import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and print output in real-time."""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        universal_newlines=True
    )
    
    # Print output in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    # Check return code
    rc = process.poll()
    if rc != 0:
        print(f"Command failed with return code {rc}")
        sys.exit(1)

def install_dlib():
    """Comprehensive Dlib installation script."""
    print("🚀 Starting Dlib Installation Process")
    
    # Ensure we have the latest pip and build tools
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    run_command(f"{sys.executable} -m pip install --upgrade setuptools wheel")
    run_command(f"{sys.executable} -m pip install cmake scikit-build")
    
    # Install system-level dependencies (Windows-specific)
    print("\n🔧 Installing system dependencies")
    run_command("pip install numpy")
    
    # Install Dlib with various options
    print("\n📦 Attempting Dlib Installation")
    install_commands = [
        f"{sys.executable} -m pip install dlib",
        f"{sys.executable} -m pip install dlib --no-cache-dir",
        f"{sys.executable} -m pip install dlib --global-option=build_ext",
        f"{sys.executable} -m pip install dlib --no-build-isolation"
    ]
    
    for cmd in install_commands:
        try:
            run_command(cmd)
            break
        except Exception as e:
            print(f"Installation method failed: {cmd}")
            print(f"Error: {e}")
    
    # Verify installation
    print("\n🕵️ Verifying Dlib Installation")
    try:
        import dlib
        print(f"✅ Dlib successfully installed! Version: {dlib.__version__}")
    except ImportError:
        print("❌ Dlib installation failed")
        sys.exit(1)

if __name__ == "__main__":
    install_dlib()
