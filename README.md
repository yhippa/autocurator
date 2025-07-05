# AutoCurator 🚗✨

**AI-Powered Car Photo Curation for Social Media**

AutoCurator uses advanced AI vision models to automatically evaluate and rank your car photos for social media appeal. Perfect for car enthusiasts who take hundreds of photos at car shows and need to quickly find the best shots for Instagram, TikTok, or other platforms.

## 🌟 Features

- **Smart Photo Ranking**: AI evaluates photos based on social media appeal, not just technical quality
- **Duplicate Detection**: Automatically groups similar shots and picks the best from each group
- **Ready-to-Use Captions**: Generates Instagram/TikTok captions with relevant hashtags
- **Multiple AI Backends**: Works with both OpenAI GPT-4V and local Ollama models
- **Batch Processing**: Evaluate entire folders of photos in one go
- **Detailed Analysis**: Get explanations for why photos scored high or low

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed with LLaVA model, OR OpenAI API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/autocurator.git
cd autocurator
```

2. **Set up virtual environment:**
```bash
python3 -m venv car_photo_env
source car_photo_env/bin/activate  # On Windows: car_photo_env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install Ollama and LLaVA (local AI option):**
```bash
# Install Ollama from https://ollama.ai/
ollama pull llava:latest
ollama serve
```

### Basic Usage

**Evaluate photos with local AI:**
```bash
./run_autocurator.sh /path/to/your/car/photos --top 10
```

**Use OpenAI GPT-4V instead:**
```bash
./run_autocurator.sh /path/to/your/car/photos --openai-api-key YOUR_API_KEY --top 10
```

**Generate captions file:**
```bash
./run_autocurator.sh /path/to/your/car/photos --captions best_captions.txt --top 5
```

**Skip duplicate detection (faster):**
```bash
./run_autocurator.sh /path/to/your/car/photos --no-duplicates --top 10
```

## 📖 Detailed Usage

### Command Line Options

```bash
python ai_photo_evaluator.py [folder] [options]

Required:
  folder                    Folder containing photos to evaluate

Options:
  -o, --output FILE        Save detailed results to JSON file
  -c, --captions FILE      Save captions for top photos to text file
  -n, --top N              Number of top photos to display (default: 10)
  --openai-api-key KEY     Use OpenAI GPT-4V instead of local Ollama
  --no-duplicates          Skip duplicate detection for faster processing
```

### Example Workflow

1. **Take 200 photos at Cars & Coffee**
2. **Run AutoCurator:**
   ```bash
   ./run_autocurator.sh ~/car_show_photos --top 10 --captions instagram_ready.txt
   ```
3. **Get results:**
   - Top 10 photos ranked by social media appeal
   - Duplicate shots automatically filtered out
   - Ready-to-use captions with hashtags
   - Detailed explanations for each photo's score

### Sample Output

```
TOP 10 PHOTOS FOR SOCIAL MEDIA
================================================================================

1. DSC_0425.JPG
   Score: 94/100
   📎 Best of 3 similar shots
      Alternatives: DSC_0426.JPG, DSC_0427.JPG
   Subject: Red Ferrari 488 GTB
   Analysis: Excellent close-up shot of a stunning Ferrari with perfect lighting...
   📱 Suggested Caption: Ferrari perfection at Cars & Coffee ✨ #Ferrari #488GTB #CarsAndCoffee #Supercar

2. DSC_0301.JPG
   Score: 87/100
   Subject: Classic Porsche 911
   Analysis: Beautiful vintage Porsche with great composition and clean background...
```

## 🔧 Technical Details

### How It Works

1. **Image Analysis**: Each photo is analyzed by AI vision models (LLaVA or GPT-4V)
2. **Social Media Scoring**: Photos are rated on factors like:
   - Car prominence and clarity
   - Visual impact and composition
   - Background quality
   - Social media appeal (would it stop someone scrolling?)
3. **Duplicate Detection**: Similar shots are grouped and the best is selected
4. **Content Generation**: Captions and hashtags are generated for top photos

### Evaluation Criteria

**Technical Requirements (must pass):**
- Photo must be sharp and in focus
- Subject must be clearly visible
- Proper exposure

**Content Evaluation:**
- Clear, interesting car as main subject
- Good lighting on the vehicle
- Clean or compelling background
- Eye-catching composition
- Social media scroll-stopping potential

### AI Models Used

- **Local Option**: Ollama + LLaVA (free, private, slower)
- **Cloud Option**: OpenAI GPT-4V (paid, faster, more accurate)

## 🛠️ Installation Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama service
ollama serve

# Verify LLaVA is installed
ollama list | grep llava
```

### Python Dependencies
```bash
# If you get import errors
pip install --upgrade pip
pip install -r requirements.txt
```

### Permission Issues
```bash
# Make script executable
chmod +x run_autocurator.sh
```

## 🚀 Future Improvements

### Planned Features
- [ ] **Content Categorization**: Group photos by car type, style, era
- [ ] **Platform-Specific Optimization**: Different scoring for Instagram vs TikTok vs YouTube
- [ ] **Auto-Crop Suggestions**: Generate crops for different aspect ratios
- [ ] **Privacy Protection**: Auto-detect and flag license plates/faces
- [ ] **Event Context**: Tailor evaluation based on detected event type
- [ ] **Batch Caption Export**: Export captions in various social media formats
- [ ] **Web Interface**: Browser-based GUI for easier use
- [ ] **Mobile App**: On-device photo curation for car shows

### Technical Improvements
- [ ] **Faster Duplicate Detection**: Use image embeddings for similarity
- [ ] **Custom Training**: Fine-tune models on car photography datasets
- [ ] **Ensemble Scoring**: Combine multiple AI models for better accuracy
- [ ] **Real-time Processing**: Live photo evaluation during shooting
- [ ] **Cloud Integration**: Direct upload to social media platforms
- [ ] **Analytics Dashboard**: Track which types of photos perform best

### Advanced Features
- [ ] **Style Transfer**: Suggest editing styles based on trending content
- [ ] **Composition Analysis**: Detailed feedback on rule of thirds, leading lines
- [ ] **Color Grading Suggestions**: Recommend color adjustments for better appeal
- [ ] **Hashtag Optimization**: Research and suggest trending hashtags
- [ ] **Performance Tracking**: Integrate with social media APIs to track actual performance

## 🤝 Contributing

Contributions are welcome! Here are some ways to help:

1. **Report Issues**: Found a bug or have a feature request? Open an issue!
2. **Improve Documentation**: Help make the README clearer or add examples
3. **Add Features**: Implement items from the future improvements list
4. **Test Different Models**: Try other Ollama models and report results
5. **Optimize Performance**: Help make duplicate detection faster
6. **Add Platform Support**: Extend for different social media platforms

### Development Setup

```bash
git clone https://github.com/yourusername/autocurator.git
cd autocurator
python3 -m venv dev_env
source dev_env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai/) and [LLaVA](https://llava-vl.github.io/)
- Inspired by the need to efficiently curate car photography for social media
- Thanks to the automotive photography community for feedback and testing

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and community chat
- **Email**: [richard.yhip@gmail.com](mailto:richard.yhip@gmail.com)

---

**⭐ If AutoCurator helps you find your best car photos, please star this repository!**