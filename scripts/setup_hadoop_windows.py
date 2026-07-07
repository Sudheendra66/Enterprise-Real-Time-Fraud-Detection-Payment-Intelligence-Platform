"""
Setup script for Hadoop/Windows compatibility for PySpark.
This script downloads winutils.exe and sets up the required directory structure.
"""
import os
import urllib.request
import zipfile
import sys


def setup_hadoop_windows():
    """Setup Hadoop binaries for Windows to enable PySpark to run."""
    
    # Default paths
    hadoop_home = os.getenv("HADOOP_HOME", "C:\\hadoop")
    hadoop_bin = os.path.join(hadoop_home, "bin")
    winutils_path = os.path.join(hadoop_bin, "winutils.exe")
    
    print(f"Setting up Hadoop for Windows...")
    print(f"HADOOP_HOME: {hadoop_home}")
    print(f"WinUtils path: {winutils_path}")
    
    # Create directory structure
    os.makedirs(hadoop_bin, exist_ok=True)
    os.makedirs(os.path.join(hadoop_home, "etc", "hadoop"), exist_ok=True)
    
    # Check if winutils.exe already exists
    if os.path.exists(winutils_path):
        print(f"✓ winutils.exe already exists at {winutils_path}")
        return True
    
    # Try to download winutils.exe
    # Hadoop 3.3.6 is commonly used with Spark 3.x
    hadoop_version = "3.3.6"
    winutils_url = f"https://github.com/cdarlint/winutils/raw/master/hadoop-{hadoop_version}/bin/winutils.exe"
    
    print(f"Downloading winutils.exe from {winutils_url}...")
    
    try:
        # Create a request with headers to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(winutils_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(winutils_path, 'wb') as f:
                f.write(response.read())
        
        print(f"✓ Successfully downloaded winutils.exe to {winutils_path}")
        
        # Create necessary Hadoop directories with proper permissions
        create_hadoop_directories(hadoop_home)
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to download winutils.exe: {e}")
        print("\nAlternative solutions:")
        print("1. Manually download winutils.exe and place it in:", hadoop_bin)
        print("2. Use a different Hadoop version from: https://github.com/cdarlint/winutils")
        print("3. Set SPARK_LOCAL_IP environment variable to bypass this check")
        return False


def create_hadoop_directories(hadoop_home):
    """Create necessary Hadoop directories."""
    dirs = [
        os.path.join(hadoop_home, "bin"),
        os.path.join(hadoop_home, "etc", "hadoop"),
        os.path.join(hadoop_home, "logs"),
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")


def setup_environment_variables():
    """Setup environment variables for Hadoop."""
    hadoop_home = os.getenv("HADOOP_HOME", "C:\\hadoop")
    hadoop_bin = os.path.join(hadoop_home, "bin")
    
    # Set environment variables
    os.environ["HADOOP_HOME"] = hadoop_home
    os.environ["hadoop.home.dir"] = hadoop_home
    os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ.get("PATH", "")
    
    print(f"\n✓ Environment variables set:")
    print(f"  HADOOP_HOME={hadoop_home}")
    print(f"  hadoop.home.dir={hadoop_home}")
    print(f"  PATH includes: {hadoop_bin}")


def main():
    """Main setup function."""
    print("=" * 60)
    print("Hadoop Windows Setup for PySpark")
    print("=" * 60)
    
    # Setup Hadoop directories and winutils
    success = setup_hadoop_windows()
    
    if success:
        # Setup environment variables
        setup_environment_variables()
        
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run: python test_spark.py")
        return 0
    else:
        print("\n" + "=" * 60)
        print("✗ Setup failed. Please follow the alternative solutions above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())