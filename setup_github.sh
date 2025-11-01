#!/bin/bash
# GitHub Setup Script for yt-stem-splitter

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║         Setting up GitHub repository: yt-stem-splitter              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Authenticate with GitHub CLI
echo "📝 Step 1: Authenticate with GitHub CLI"
echo "----------------------------------------"
echo "You need to authenticate with GitHub CLI first."
echo "Run this command:"
echo ""
echo "  gh auth login"
echo ""
echo "Follow the prompts to:"
echo "  1. Choose GitHub.com"
echo "  2. Choose HTTPS or SSH"
echo "  3. Authenticate via browser or token"
echo ""
read -p "Press Enter after you've authenticated with 'gh auth login'..."

# Verify authentication
echo ""
echo "Verifying authentication..."
if gh auth status; then
    echo "✅ Authentication successful!"
else
    echo "❌ Authentication failed. Please run 'gh auth login' manually."
    exit 1
fi

echo ""
echo "📦 Step 2: Initialize Git Repository"
echo "----------------------------------------"

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
.pytest_cache/
htmlcov/
.coverage
*.egg-info/
dist/
build/

# Virtual environments
demucs-env/
venv/
env/

# IDEs
.vscode/
.idea/

# OS
.DS_Store

# Project specific
demucs_output/
*.wav
*.mp3
EOF
    echo "✅ .gitignore created"
fi

echo ""
echo "📝 Step 3: Stage and Commit Files"
echo "----------------------------------------"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: YouTube audio processing toolkit with stem separation

- YouTube audio download using yt-dlp
- BPM and key detection with Essentia
- Audio stem separation with Demucs
- TuneBat metadata scraping
- Comprehensive test suite (50+ tests)
- Modular architecture
- CLI and library usage modes
- Complete documentation" || echo "Files already committed"

echo "✅ Files committed"

echo ""
echo "🚀 Step 4: Create GitHub Repository"
echo "----------------------------------------"

# Create GitHub repository using gh CLI
echo "Creating repository 'yt-stem-splitter'..."
gh repo create yt-stem-splitter \
    --public \
    --description "Python toolkit for YouTube audio download, BPM/key detection, and audio stem separation using Demucs" \
    --source=. \
    --remote=origin \
    --push

echo "✅ Repository created and pushed!"

echo ""
echo "🎉 Step 5: Configure Repository"
echo "----------------------------------------"

# Add topics/tags
echo "Adding topics to repository..."
gh repo edit --add-topic python --add-topic audio-processing --add-topic youtube \
    --add-topic demucs --add-topic music --add-topic bpm-detection --add-topic audio-analysis

echo "✅ Topics added"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    🎉 SUCCESS! 🎉                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your repository has been created and pushed to GitHub!"
echo ""
echo "Repository URL:"
gh repo view --web --json url -q .url || gh repo view
echo ""
echo "Next steps:"
echo "  1. Visit your repository on GitHub"
echo "  2. Enable Issues (if not already enabled)"
echo "  3. Add a project description"
echo "  4. Consider adding:"
echo "     - CODE_OF_CONDUCT.md"
echo "     - GitHub Actions for CI/CD"
echo "     - Badges to README.md"
echo ""
echo "To view your repo in browser, run:"
echo "  gh repo view --web"
echo ""

