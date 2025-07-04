#!/usr/bin/env python3
"""
Test script to verify Borel Docker setup.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_docker_available():
    """Test if Docker is available and running."""
    print("Testing Docker availability...")
    
    success, stdout, stderr = run_command("docker --version")
    if not success:
        print("❌ Docker is not installed or not in PATH")
        return False
    
    print(f"✅ Docker is available: {stdout.strip()}")
    
    success, stdout, stderr = run_command("docker info")
    if not success:
        print("❌ Docker is not running. Please start Docker Desktop.")
        return False
    
    print("✅ Docker is running")
    return True

def test_docker_build():
    """Test if the Docker image can be built."""
    print("\nTesting Docker build...")
    
    success, stdout, stderr = run_command("docker build -t borel:test .")
    if not success:
        print("❌ Docker build failed")
        print(f"Error: {stderr}")
        return False
    
    print("✅ Docker image built successfully")
    
    # Clean up test image
    run_command("docker rmi borel:test")
    return True

def test_docker_run():
    """Test if the Docker container can run."""
    print("\nTesting Docker run...")
    
    # Create a simple test markdown file
    test_md = Path("test-docker.md")
    test_md.write_text("""---
title: Docker Test
author: Test User
date: 2024-01-15
---

# Docker Test

This is a test document to verify Docker functionality.

## Features

- Docker containerization
- Markdown processing
- PDF generation
""")
    
    try:
        # Run borel in Docker
        success, stdout, stderr = run_command(
            "docker run --rm -v \"$(pwd):/workspace\" -w /workspace borel:test test-docker.md"
        )
        
        if not success:
            print("❌ Docker run failed")
            print(f"Error: {stderr}")
            return False
        
        print("✅ Docker run successful")
        
        # Check if PDF was generated
        test_pdf = Path("test-docker.pdf")
        if test_pdf.exists():
            print("✅ PDF file generated successfully")
            # Clean up test files
            test_md.unlink()
            test_pdf.unlink()
            return True
        else:
            print("❌ PDF file was not generated")
            return False
            
    except Exception as e:
        print(f"❌ Docker run failed with exception: {e}")
        return False

def test_wrapper_script():
    """Test if the wrapper script works."""
    print("\nTesting wrapper script...")
    
    script_path = Path("scripts/borel-docker.sh")
    if not script_path.exists():
        print("❌ Wrapper script not found")
        return False
    
    if not os.access(script_path, os.X_OK):
        print("❌ Wrapper script is not executable")
        return False
    
    success, stdout, stderr = run_command("./scripts/borel-docker.sh --help")
    if not success:
        print("❌ Wrapper script failed")
        print(f"Error: {stderr}")
        return False
    
    print("✅ Wrapper script works correctly")
    return True

def main():
    """Run all Docker tests."""
    print("Borel Docker Test")
    print("=" * 50)
    
    tests = [
        test_docker_available,
        test_docker_build,
        test_docker_run,
        test_wrapper_script
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Docker Test Results Summary:")
    
    if all(results):
        print("✅ All Docker tests passed! Borel Docker setup is working.")
        print("\nYou can now use:")
        print("  ./scripts/borel-docker.sh input.md")
        print("  ./scripts/borel-docker.sh --help")
        return 0
    else:
        print("❌ Some Docker tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure Docker Desktop is installed and running")
        print("2. Check that you have sufficient disk space")
        print("3. Verify network connectivity for Docker builds")
        print("4. See DOCKER.md for detailed troubleshooting")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 