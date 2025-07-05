# Contributing to AutoCurator

We love contributions! AutoCurator is a community-driven project that helps car enthusiasts efficiently curate their photos for social media.

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/autocurator.git
   cd autocurator
   ```
3. **Set up development environment:**
   ```bash
   ./setup.sh
   ```
4. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make your changes and test them**
6. **Submit a pull request**

## 🛠️ Ways to Contribute

### 🐛 Report Bugs
- Use the issue tracker to report bugs
- Include steps to reproduce, expected vs actual behavior
- Add photos/examples if helpful (remove any private info)

### 💡 Suggest Features
- Check existing issues first to avoid duplicates
- Explain the use case and why it would be valuable
- Consider implementation complexity and user experience

### 📝 Improve Documentation
- Fix typos, clarify instructions
- Add examples and use cases
- Improve README organization
- Write guides for specific workflows

### 🔧 Code Contributions

**High-Impact Areas:**
- **Performance**: Make duplicate detection faster
- **Accuracy**: Improve photo ranking algorithm
- **Usability**: Better error messages, progress indicators
- **Features**: Platform-specific optimization, content categorization
- **Testing**: Add unit tests, integration tests

**Code Style:**
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Keep functions focused and small

## 🧪 Testing Your Changes

1. **Test with sample photos:**
   ```bash
   # Create test folder with 10-20 car photos
   ./run_autocurator.sh test_photos --top 5
   ```

2. **Test edge cases:**
   - Very large photos (>20MB)
   - Corrupted image files
   - Folders with no images
   - Network connectivity issues

3. **Test both AI backends:**
   ```bash
   # Test with Ollama
   ./run_autocurator.sh test_photos --top 5
   
   # Test with OpenAI (if you have API key)
   ./run_autocurator.sh test_photos --openai-api-key YOUR_KEY --top 5
   ```

## 📋 Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add tests** for new features when possible
3. **Update README.md** if you've added new command line options
4. **Test thoroughly** with different photo sets and conditions
5. **Write clear commit messages** describing what and why

### Good Commit Messages
```
✅ Good:
- Add content categorization for different car types
- Fix duplicate detection infinite loop bug
- Improve error handling for corrupted images

❌ Avoid:
- Update code
- Fix stuff
- WIP
```

## 🎯 Priority Areas for Contribution

### 🔥 High Priority
1. **Faster Duplicate Detection**: Current approach is slow for large sets
2. **Better Photo Ranking**: Fine-tune scoring algorithm based on real social media performance
3. **Error Recovery**: Better handling of failed AI responses
4. **Progress Indicators**: Show progress for long-running operations

### 🚀 Medium Priority
1. **Platform Optimization**: Different scoring for Instagram vs TikTok
2. **Content Categorization**: Group by car type, era, style
3. **Auto-crop Suggestions**: Generate crops for different aspect ratios
4. **Batch Operations**: Process multiple folders efficiently

### 💡 Ideas Welcome
1. **Web Interface**: Browser-based GUI
2. **Mobile App**: On-device curation
3. **Cloud Integration**: Direct social media posting
4. **Analytics**: Track which photo types perform best

## 🤝 Community Guidelines

- **Be respectful** and constructive in discussions
- **Help newcomers** learn the codebase
- **Focus on the user experience** - car enthusiasts with limited time
- **Consider performance** - users may have hundreds of photos
- **Think about privacy** - users' car photos may contain personal info

## 🛡️ Testing with Real Data

When testing, be mindful that:
- Car photos may contain license plates or personal info
- Large photo sets (200+ images) stress-test the system
- Different camera settings and lighting conditions affect AI performance
- Various car types (classics, supercars, modified, stock) should all work well

## 📞 Getting Help

- **Questions about contributing?** Open a GitHub Discussion
- **Need technical help?** Comment on relevant issues
- **Want to pair program?** Mention it in issues - many contributors are happy to help

## 🏆 Recognition

Contributors will be:
- Added to the README acknowledgments
- Mentioned in release notes for significant contributions
- Invited to help guide the project's direction

---

**Thank you for helping make AutoCurator better for the car community! 🚗✨**