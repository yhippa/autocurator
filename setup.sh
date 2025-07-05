#!/bin/bash
# AutoCurator Setup Script

echo "🚗 AutoCurator Setup"
echo "===================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv car_photo_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source car_photo_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Python setup complete!"
echo ""

# Check for Ollama
echo "🤖 Checking AI backend options..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if ollama is running
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "✅ Ollama is running"
        
        # Check for LLaVA model
        if ollama list | grep -q llava; then
            echo "✅ LLaVA model is installed"
        else
            echo "📥 Installing LLaVA model (this may take a few minutes)..."
            ollama pull llava:latest
        fi
    else
        echo "⚠️  Ollama is installed but not running"
        echo "Start it with: ollama serve"
    fi
else
    echo "⚠️  Ollama not found"
    echo "For local AI, install from: https://ollama.ai/"
    echo "Or use --openai-api-key with the script"
fi

# Make script executable
chmod +x run_autocurator.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. If using Ollama: ollama serve"
echo "2. Test with: ./run_autocurator.sh /path/to/car/photos --top 5"
echo "3. For OpenAI: ./run_autocurator.sh /path/to/photos --openai-api-key YOUR_KEY"
echo ""
echo "For help: ./run_autocurator.sh --help"