#!/bin/bash

# Support Agent Installation Script
# This script sets up the Support Agent environment

echo "🚀 Support Agent Installation Script"
echo "===================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1)
if [[ $python_version == *"Python 3."* ]]; then
    echo "✅ Python found: $python_version"
else
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "support_agent_env" ]; then
    python -m venv support_agent_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source support_agent_env/Scripts/activate
else
    # macOS/Linux
    source support_agent_env/bin/activate
fi
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for API key
echo ""
echo "Checking for Gemini API key..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY environment variable not set"
    echo "   Please set your Gemini API key:"
    echo "   export GEMINI_API_KEY='your_api_key_here'"
    echo ""
    echo "   Or update the config.py file with your API key"
else
    echo "✅ Gemini API key found"
fi

# Run health check
echo ""
echo "Running health check..."
python main.py --health-check
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "Quick start commands:"
    echo "  python main.py                    # Run default example"
    echo "  python main.py --test             # Run test scenarios" 
    echo "  python main.py --interactive      # Interactive mode"
    echo "  python main.py --help             # Show all options"
else
    echo ""
    echo "❌ Health check failed. Please check the error messages above."
fi
