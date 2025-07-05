#!/bin/bash
# AutoCurator Example Usage
# This script demonstrates various ways to use AutoCurator

echo "🚗 AutoCurator Example Usage"
echo "============================="
echo ""

# Check if we have a test folder
if [ ! -d "example_photos" ]; then
    echo "📂 No example_photos folder found."
    echo ""
    echo "To run these examples:"
    echo "1. Create a folder called 'example_photos'"
    echo "2. Add 10-20 car photos to it"
    echo "3. Run this script again"
    echo ""
    echo "Or replace 'example_photos' below with your photo folder path."
    exit 1
fi

PHOTO_DIR="example_photos"
echo "📸 Using photos from: $PHOTO_DIR"
echo ""

# Basic usage - top 5 photos
echo "🥇 Example 1: Get top 5 photos"
echo "Command: ./run_autocurator.sh $PHOTO_DIR --top 5"
echo ""
./run_autocurator.sh "$PHOTO_DIR" --top 5
echo ""
echo "Press Enter to continue to next example..."
read

# Generate captions
echo "📱 Example 2: Generate social media captions"
echo "Command: ./run_autocurator.sh $PHOTO_DIR --top 3 --captions example_captions.txt"
echo ""
./run_autocurator.sh "$PHOTO_DIR" --top 3 --captions example_captions.txt
echo ""
echo "📄 Captions saved to: example_captions.txt"
cat example_captions.txt
echo ""
echo "Press Enter to continue to next example..."
read

# Save detailed results
echo "💾 Example 3: Save detailed results to JSON"
echo "Command: ./run_autocurator.sh $PHOTO_DIR --top 5 --output detailed_results.json"
echo ""
./run_autocurator.sh "$PHOTO_DIR" --top 5 --output detailed_results.json
echo ""
echo "📄 Detailed results saved to: detailed_results.json"
echo "First few lines:"
head -20 detailed_results.json
echo ""
echo "Press Enter to continue to next example..."
read

# Skip duplicate detection for speed
echo "⚡ Example 4: Skip duplicate detection (faster)"
echo "Command: ./run_autocurator.sh $PHOTO_DIR --no-duplicates --top 5"
echo ""
./run_autocurator.sh "$PHOTO_DIR" --no-duplicates --top 5
echo ""

echo "✅ Examples complete!"
echo ""
echo "🎯 Try these commands with your own photos:"
echo "  ./run_autocurator.sh /path/to/your/car/photos --top 10"
echo "  ./run_autocurator.sh /path/to/your/car/photos --captions instagram_ready.txt --top 5"
echo ""
echo "📚 For more options: ./run_autocurator.sh --help"