#!/usr/bin/env python3
"""
Voice Conversion System - Development Status Checker
Quick script to check what's working and what needs to be implemented
"""

import sys
import os
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status"""
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_directory_exists(dir_path, description):
    """Check if a directory exists and report status"""
    exists = Path(dir_path).exists() and Path(dir_path).is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dir_path}")
    return exists

def check_import(module_path, description):
    """Try to import a module and report status"""
    try:
        exec(f"import {module_path}")
        print(f"✅ {description}: {module_path}")
        return True
    except ImportError as e:
        print(f"❌ {description}: {module_path} - {e}")
        return False
    except Exception as e:
        print(f"⚠️  {description}: {module_path} - {e}")
        return False

def main():
    """Main status check function"""
    print("🔍 Voice Conversion System - Development Status Check")
    print("=" * 60)
    
    base_dir = Path(__file__).parent / "voice_conversion_system"
    
    # Check project structure
    print("\n📁 Project Structure:")
    structure_ok = True
    structure_ok &= check_directory_exists(base_dir / "src", "Source directory")
    structure_ok &= check_directory_exists(base_dir / "src" / "api", "API module")
    structure_ok &= check_directory_exists(base_dir / "src" / "core", "Core module")
    structure_ok &= check_directory_exists(base_dir / "src" / "models", "Models module")
    structure_ok &= check_directory_exists(base_dir / "src" / "pipeline", "Pipeline module")
    structure_ok &= check_directory_exists(base_dir / "config", "Config directory")
    
    # Check configuration files
    print("\n⚙️  Configuration Files:")
    config_ok = True
    config_ok &= check_file_exists(base_dir / "config" / "system_config.yaml", "System config")
    config_ok &= check_file_exists(base_dir / "config" / "model_config.yaml", "Model config")
    config_ok &= check_file_exists(base_dir / "requirements.txt", "Requirements file")
    
    # Check setup directories
    print("\n📂 Setup Directories:")
    dirs_ok = True
    dirs_ok &= check_directory_exists(base_dir / "cache", "Cache directory")
    dirs_ok &= check_directory_exists(base_dir / "temp", "Temp directory")
    dirs_ok &= check_directory_exists(base_dir / "logs", "Logs directory")
    dirs_ok &= check_directory_exists(base_dir / "models", "Models directory")
    
    # Check key Python files
    print("\n🐍 Key Python Files:")
    files_ok = True
    files_ok &= check_file_exists(base_dir / "src" / "api" / "main.py", "API main")
    files_ok &= check_file_exists(base_dir / "src" / "pipeline" / "conversion_pipeline.py", "Conversion pipeline")
    files_ok &= check_file_exists(base_dir / "src" / "core" / "config.py", "Config loader")
    
    # Try basic imports (these will likely fail without dependencies)
    print("\n📦 Basic Dependencies:")
    # Add the src directory to Python path for testing
    sys.path.insert(0, str(base_dir))
    
    deps_ok = True
    deps_ok &= check_import("yaml", "PyYAML")
    deps_ok &= check_import("pathlib", "Pathlib")
    
    # Try to import our modules (will fail if dependencies missing)
    print("\n🔧 Our Modules (may fail without dependencies):")
    modules_ok = True
    try:
        from src.core.config import Config
        print("✅ Core config module: Can be imported")
        modules_ok = True
    except Exception as e:
        print(f"❌ Core config module: {e}")
        modules_ok = False
    
    # Overall status
    print("\n" + "=" * 60)
    print("📊 OVERALL STATUS:")
    
    if structure_ok and config_ok and dirs_ok and files_ok:
        print("✅ BASIC SETUP: Complete")
    else:
        print("❌ BASIC SETUP: Issues found")
    
    if deps_ok:
        print("✅ BASIC DEPENDENCIES: Available")
    else:
        print("❌ BASIC DEPENDENCIES: Missing - run 'pip install -r requirements.txt'")
    
    if modules_ok:
        print("✅ CORE MODULES: Can be imported")
    else:
        print("❌ CORE MODULES: Import issues - likely need dependencies")
    
    print("\n🎯 WHAT TO DO NEXT:")
    if not (structure_ok and config_ok and dirs_ok and files_ok):
        print("1. 🔧 Fix basic setup issues above")
    elif not deps_ok:
        print("1. 📦 Install dependencies: pip install -r voice_conversion_system/requirements.txt")
    elif not modules_ok:
        print("1. 🔍 Check dependency issues and fix import problems")
    else:
        print("1. ✨ Basic setup looks good! Check NEXT_STEPS.md for development priorities")
        print("2. 🚀 Start implementing missing model components")
        print("3. 🧪 Create tests and verify functionality")
    
    print("\n📖 For detailed guidance, see: NEXT_STEPS.md")

if __name__ == "__main__":
    main()