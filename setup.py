#!/usr/bin/env python3
"""
Quick setup script for Voice Conversion System
Run this to set up the basic development environment
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create required directories"""
    base_dir = Path(__file__).parent / "voice_conversion_system"
    
    directories = [
        "cache",
        "temp", 
        "logs",
        "models/voice_library",
        "models/voice_converter",
        "models/vocoder",
        "test_data"
    ]
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {full_path}")

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required packages"""
    import subprocess
    
    requirements_file = Path(__file__).parent / "voice_conversion_system" / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    try:
        print("📦 Installing dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_imports():
    """Test if core modules can be imported"""
    try:
        # Test core Python imports
        import yaml
        import numpy as np
        import torch
        print("✓ Core dependencies available")
        
        # Test if we can import our modules (will fail initially but that's expected)
        sys.path.insert(0, str(Path(__file__).parent / "voice_conversion_system"))
        try:
            from src.core.config import Config
            print("✓ Config module can be imported")
        except Exception as e:
            print(f"⚠️  Config module import failed (expected): {e}")
        
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def create_sample_config():
    """Create a sample configuration for testing"""
    config_dir = Path(__file__).parent / "voice_conversion_system" / "config"
    sample_config = config_dir / "sample_test_config.yaml"
    
    sample_content = """
# Sample configuration for testing
models:
  speaker_encoder_model: "resemblyzer"
  content_encoder_model: "facebook/wav2vec2-base-960h"
  voice_converter_model: "autovc"
  vocoder_model: "hifigan"
  sample_rate: 16000
  hop_length: 256
  win_length: 1024
  n_mels: 80

processing:
  chunk_duration: 10.0
  overlap_duration: 1.0
  max_audio_length: 60
  min_target_duration: 3.0
  noise_threshold: 10.0

system:
  cache_dir: "cache"
  temp_dir: "temp"
  voice_library_dir: "models/voice_library"
  log_level: "INFO"
  log_file: "logs/voice_conversion.log"
  max_workers: 4
"""
    
    with open(sample_config, 'w') as f:
        f.write(sample_content)
    
    print(f"✓ Created sample config: {sample_config}")

def main():
    """Main setup function"""
    print("🚀 Setting up Voice Conversion System...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Create sample config
    create_sample_config()
    
    # Install dependencies (optional - can be time consuming)
    install_deps = input("\n📦 Install dependencies now? (y/N): ").lower().strip()
    if install_deps == 'y':
        if not install_dependencies():
            print("\n⚠️  Dependency installation failed. You can install manually with:")
            print("pip install -r voice_conversion_system/requirements.txt")
    else:
        print("\n📝 To install dependencies later, run:")
        print("pip install -r voice_conversion_system/requirements.txt")
    
    # Test imports
    print("\n🧪 Testing imports...")
    test_imports()
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Install dependencies if you haven't already")
    print("2. Check the NEXT_STEPS.md file for detailed guidance")
    print("3. Start with: python -c \"from voice_conversion_system.src.api.main import app; print('API setup successful')\"")
    
    return True

if __name__ == "__main__":
    main()