#!/usr/bin/env python3
"""
Script to clean API keys from Git history
This script uses git filter-repo to remove sensitive information from all commits.
"""

import subprocess
import sys
import os

def clean_git_history():
    """Remove API keys from Git history"""
    print("🧹 Cleaning Git history of API keys...")
    
    # Create a backup branch first
    try:
        subprocess.run(["git", "branch", "backup-before-clean"], check=True)
        print("✅ Created backup branch: backup-before-clean")
    except subprocess.CalledProcessError:
        print("⚠️  Backup branch already exists")
    
    # Use git filter-repo to remove API keys
    # This will rewrite the entire Git history
    try:
        # Remove the specific API key pattern
        cmd = [
            "git", "filter-repo",
            "--replace-text", "replacements.txt",
            "--force"
        ]
        
        # Create replacements file
        with open("replacements.txt", "w") as f:
            f.write("REMOVED_API_KEY==>REMOVED_API_KEY\n")
            f.write("REMOVED_API_KEY==>REMOVED_API_KEY\n")  # Generic pattern for any sk-proj keys
        
        print("🔍 Running git filter-repo to clean history...")
        subprocess.run(cmd, check=True)
        
        # Clean up
        os.remove("replacements.txt")
        
        print("✅ Successfully cleaned Git history!")
        print("📝 Next steps:")
        print("1. Force push to remote: git push --force origin main")
        print("2. Delete backup branch if everything looks good: git branch -D backup-before-clean")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error cleaning history: {e}")
        print("You can restore from backup with: git checkout backup-before-clean")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("🔍 Dry run mode - would clean history but not execute")
        print("To actually clean history, run: python clean_history.py")
    else:
        clean_git_history() 