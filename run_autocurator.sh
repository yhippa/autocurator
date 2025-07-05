#!/bin/bash
# AutoCurator - AI-Powered Car Photo Curation
# https://github.com/yourusername/autocurator

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/car_photo_env" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please set up the environment first:"
    echo "  python3 -m venv car_photo_env"
    echo "  source car_photo_env/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    echo "For Ollama (local AI):"
    echo "  ollama pull llava:latest"
    echo "  ollama serve"
    exit 1
fi

# Activate virtual environment
source "$SCRIPT_DIR/car_photo_env/bin/activate"

# Check if Ollama is running (if no OpenAI API key provided)
if [[ ! "$*" == *"--openai-api-key"* ]]; then
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "⚠️  Ollama doesn't seem to be running."
        echo "Start it with: ollama serve"
        echo "Or use --openai-api-key to use OpenAI instead."
        echo ""
        echo "Continuing anyway (will show error if Ollama is really not available)..."
    fi
fi

echo "🚗 AutoCurator - AI-Powered Car Photo Curation"
echo ""

# Run the AI photo evaluator with all arguments passed through
python "$SCRIPT_DIR/ai_photo_evaluator.py" "$@"