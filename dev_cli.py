#!/usr/bin/env python3
"""
Voice Conversion System - Development CLI
Simple command-line interface for development and testing
"""

import argparse
import sys
from pathlib import Path

def cmd_status():
    """Show system status"""
    print("🔍 Running system status check...")
    import subprocess
    result = subprocess.run([sys.executable, "check_status.py"], cwd=Path(__file__).parent)
    return result.returncode == 0

def cmd_setup():
    """Run system setup"""
    print("🚀 Running system setup...")
    import subprocess
    result = subprocess.run([sys.executable, "setup.py"], cwd=Path(__file__).parent)
    return result.returncode == 0

def cmd_install():
    """Install dependencies"""
    print("📦 Installing dependencies...")
    import subprocess
    requirements_file = Path(__file__).parent / "voice_conversion_system" / "requirements.txt"
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
    ])
    return result.returncode == 0

def cmd_test_api():
    """Test if API can start"""
    print("🧪 Testing API startup...")
    try:
        # Add path for imports
        sys.path.insert(0, str(Path(__file__).parent / "voice_conversion_system"))
        
        from src.api.main import app
        print("✅ API imports successfully!")
        print("ℹ️  To start the server, run:")
        print("   uvicorn src.api.main:app --reload")
        print("   (from the voice_conversion_system directory)")
        return True
    except Exception as e:
        print(f"❌ API import failed: {e}")
        print("💡 Try installing dependencies first: python dev_cli.py install")
        return False

def cmd_next_steps():
    """Show next steps guide"""
    next_steps_file = Path(__file__).parent / "NEXT_STEPS.md"
    if next_steps_file.exists():
        print("📖 Opening next steps guide...")
        with open(next_steps_file, 'r') as f:
            content = f.read()
        
        # Show first 50 lines to avoid overwhelming output
        lines = content.split('\n')
        for i, line in enumerate(lines[:50]):
            print(line)
        
        if len(lines) > 50:
            print(f"\n... ({len(lines) - 50} more lines)")
            print(f"📄 Read the full guide: {next_steps_file}")
    else:
        print("❌ NEXT_STEPS.md not found")
        return False

def cmd_quick_start():
    """Quick start workflow"""
    print("🚀 Voice Conversion System - Quick Start")
    print("=" * 50)
    
    # Run status check
    print("\n1️⃣ Checking system status...")
    if not cmd_status():
        print("❌ Status check failed")
        return False
    
    # Test API
    print("\n2️⃣ Testing API...")
    if not cmd_test_api():
        print("⚠️  API test failed - may need dependencies")
    
    print("\n3️⃣ What to do next:")
    print("✅ Basic setup is complete!")
    print("📖 Read detailed roadmap: python dev_cli.py next-steps")
    print("📦 Install dependencies: python dev_cli.py install")
    print("🔍 Check status anytime: python dev_cli.py status")
    
    return True

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Voice Conversion System Development CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dev_cli.py quick-start    # Complete quick start workflow
  python dev_cli.py status         # Check system status
  python dev_cli.py install        # Install dependencies
  python dev_cli.py test-api       # Test API startup
  python dev_cli.py next-steps     # Show development roadmap
        """
    )
    
    parser.add_argument(
        'command',
        choices=['quick-start', 'status', 'setup', 'install', 'test-api', 'next-steps'],
        help='Command to run'
    )
    
    if len(sys.argv) == 1:
        # No arguments provided, show help and run quick-start
        parser.print_help()
        print("\n" + "="*50)
        print("Running quick-start workflow...")
        cmd_quick_start()
        return
    
    args = parser.parse_args()
    
    # Execute command
    commands = {
        'quick-start': cmd_quick_start,
        'status': cmd_status,
        'setup': cmd_setup,
        'install': cmd_install,
        'test-api': cmd_test_api,
        'next-steps': cmd_next_steps,
    }
    
    success = commands[args.command]()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()