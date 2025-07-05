#!/usr/bin/env python3
"""
AI-Powered Car Photo Evaluator
Uses modern vision AI to understand photo content and quality for social media
"""

import os
import base64
import json
from pathlib import Path
import requests
from typing import List, Dict, Tuple
import argparse

class AIPhotoEvaluator:
    def __init__(self, api_key=None, detect_duplicates=True):
        """Initialize with OpenAI API key or use local ollama"""
        self.api_key = api_key
        self.use_openai = api_key is not None
        self.detect_duplicates = detect_duplicates
        
    def encode_image(self, image_path):
        """Encode image to base64 with validation"""
        try:
            # Check file size (limit to 20MB for Ollama)
            file_size = os.path.getsize(image_path)
            if file_size > 20 * 1024 * 1024:
                print(f"⚠️  Warning: {os.path.basename(image_path)} is {file_size/(1024*1024):.1f}MB (large file)")
            
            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded
        except Exception as e:
            print(f"❌ Error encoding {os.path.basename(image_path)}: {e}")
            return None
    
    def evaluate_with_openai(self, image_path):
        """Evaluate using GPT-4V"""
        base64_image = self.encode_image(image_path)
        
        prompt = """Rate this car photo for social media appeal (Instagram/TikTok) on a scale of 1-100.

TECHNICAL REQUIREMENTS (must pass or score drops to 30 or below):
- Photo must be sharp and in focus
- Subject must be clearly visible
- No excessive blur or camera shake
- Acceptable exposure (not too dark/bright to see details)

CONTENT EVALUATION (if technical requirements are met):
- Is there a clear, interesting car as the main subject?
- Is the car well-lit and prominently featured?
- Is the background clean or does it add to the photo?
- Would this stop someone scrolling on social media?
- Does it showcase the car's best features?
- Is the composition engaging?

HEAVY PENALTIES for:
- Blurry, out-of-focus, or unclear subjects
- Photos that are mostly parking lot/background
- Distant cars that aren't the clear focus
- Cluttered scenes where the car gets lost
- Poor lighting on the car itself
- Boring angles or compositions

A blurry photo of a Ferrari should score lower than a sharp photo of a Camry.

Respond with ONLY a JSON object:
{
  "score": [1-100],
  "reasoning": "Brief explanation of why this score",
  "main_subject": "What is the primary subject of this photo",
  "social_media_appeal": "Why this would/wouldn't work for social media",
  "improvements": "What could make this photo better",
  "caption": "Ready-to-use Instagram/social media caption with relevant hashtags"
}"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Try to extract JSON from the response
                if '{' in content and '}' in content:
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    json_str = content[json_start:json_end]
                    return json.loads(json_str)
                else:
                    return {"score": 50, "reasoning": "Could not parse AI response", "error": content}
            else:
                return {"score": 0, "reasoning": f"API Error: {response.status_code}", "error": response.text}
                
        except Exception as e:
            return {"score": 0, "reasoning": f"Error: {str(e)}"}
    
    def evaluate_with_ollama(self, image_path):
        """Evaluate using local Ollama with vision model"""
        base64_image = self.encode_image(image_path)
        
        prompt = """Rate this car photo for social media appeal on a scale of 1-100.

TECHNICAL REQUIREMENTS FIRST:
✓ Photo must be sharp and clear
✓ Subject must be in focus
✓ No excessive blur or camera shake
✓ Proper exposure (can see details)

If photo fails technical requirements, score 30 or below.

IF TECHNICAL QUALITY IS GOOD, then consider:
✓ Clear, interesting car as main subject
✓ Good lighting on the car
✓ Clean or interesting background
✓ Eye-catching composition
✓ Would make people stop scrolling

Avoid:
✗ Blurry or out-of-focus photos
✗ Mostly parking lot/background
✗ Distant, unclear cars
✗ Cluttered, busy scenes
✗ Poor car lighting
✗ Boring compositions

Remember: A sharp photo of an average car beats a blurry photo of an amazing car for social media.

Give a score 1-100 and brief reasoning. Focus on social media appeal, not just technical quality.

Also create a ready-to-use social media caption with relevant hashtags for this photo."""

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llava:latest',
                    'prompt': prompt,
                    'images': [base64_image],
                    'stream': False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Try to extract score from response
                score = 50  # default
                if 'score' in response_text.lower():
                    import re
                    score_match = re.search(r'(\d+)(?:/100)?', response_text)
                    if score_match:
                        score = min(100, max(1, int(score_match.group(1))))
                
                return {
                    "score": score,
                    "reasoning": response_text,
                    "main_subject": "Analysis via Ollama",
                    "social_media_appeal": response_text
                }
            else:
                return {"score": 0, "reasoning": f"Ollama error: {response.status_code}"}
                
        except requests.exceptions.ConnectionError:
            return {"score": 0, "reasoning": "Ollama not running. Start with: ollama serve"}
        except Exception as e:
            return {"score": 0, "reasoning": f"Error: {str(e)}"}
    
    def are_photos_similar(self, image_path1, image_path2):
        """Check if two photos are similar shots of the same subject"""
        if not self.detect_duplicates:
            return False
        
        # Don't compare if either image failed to load during evaluation
        # This prevents false positives from failed images
        if not os.path.exists(image_path1) or not os.path.exists(image_path2):
            return False
            
        base64_image1 = self.encode_image(image_path1)
        base64_image2 = self.encode_image(image_path2)
        
        if base64_image1 is None or base64_image2 is None:
            return False
        
        prompt = """Compare these two car photos. Are they similar shots of the same car/subject from similar angles?

Consider them SIMILAR only if:
- Same specific car, similar angle/composition
- Multiple shots of the exact same vehicle with minor differences
- Same scene with only small changes in framing

Consider them DIFFERENT if:
- Different cars entirely (even if similar models)
- Same car but very different angles (front vs rear, close-up vs wide shot)
- Different scenes/locations
- One shows interior, other shows exterior
- Significantly different compositions

Be CONSERVATIVE - when in doubt, consider them DIFFERENT.

Respond with only: SIMILAR or DIFFERENT"""

        if self.use_openai:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image1}"}},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image2}"}}
                        ]
                    }
                ],
                "max_tokens": 50
            }
            
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    content = response.json()['choices'][0]['message']['content'].strip().upper()
                    # Be conservative - only return True if explicitly SIMILAR
                    return content == "SIMILAR"
                else:
                    return False
                    
            except Exception as e:
                print(f"   ⚠️  Error comparing {os.path.basename(image_path1)} & {os.path.basename(image_path2)}: {e}")
                return False
        else:
            # Use Ollama with LLaVA - but it's less reliable for comparisons
            try:
                response = requests.post(
                    'http://localhost:11434/api/generate',
                    json={
                        'model': 'llava:latest',
                        'prompt': prompt,
                        'images': [base64_image1, base64_image2],
                        'stream': False
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get('response', '').strip().upper()
                    # Be very conservative with Ollama - only trust clear SIMILAR responses
                    return "SIMILAR" in response_text and "DIFFERENT" not in response_text
                else:
                    return False
                    
            except Exception as e:
                print(f"   ⚠️  Error comparing with Ollama: {e}")
                return False
        
        return False
    
    def group_similar_photos(self, results):
        """Group similar photos and return the best from each group"""
        if not self.detect_duplicates or len(results) < 2:
            return results
            
        print(f"\n🔍 Checking for duplicate/similar shots among {len(results)} photos...")
        
        # Filter out failed photos first
        valid_results = [r for r in results if r.get('score', 0) > 0]
        failed_results = [r for r in results if r.get('score', 0) == 0]
        
        if len(valid_results) < 2:
            print("   ⚠️  Too few valid photos for duplicate detection")
            return results
        
        groups = []
        processed = set()
        comparison_count = 0
        max_comparisons = len(valid_results) * 5  # Safety limit
        
        for i, result1 in enumerate(valid_results):
            if result1['path'] in processed:
                continue
                
            # Start a new group with this photo
            current_group = [result1]
            processed.add(result1['path'])
            
            # Find all similar photos
            for j, result2 in enumerate(valid_results[i+1:], i+1):
                if result2['path'] in processed:
                    continue
                
                # Safety check - limit total comparisons to prevent runaway processing
                comparison_count += 1
                if comparison_count > max_comparisons:
                    print(f"   ⚠️  Stopping duplicate detection after {comparison_count} comparisons (safety limit)")
                    break
                
                # Limit group size - if we already have 10 in a group, something's wrong
                if len(current_group) >= 10:
                    print(f"   ⚠️  Group too large ({len(current_group)} photos), stopping growth")
                    break
                
                if self.are_photos_similar(result1['path'], result2['path']):
                    current_group.append(result2)
                    processed.add(result2['path'])
                    print(f"   📎 Found similar: {result1['file']} & {result2['file']}")
            
            groups.append(current_group)
            
            # If this group got suspiciously large, stop processing
            if len(current_group) > 5:
                print(f"   ⚠️  Large group detected ({len(current_group)} photos), may indicate comparison issues")
        
        # Add any unprocessed photos as individual groups
        for result in valid_results:
            if result['path'] not in processed:
                groups.append([result])
        
        # From each group, pick the highest scoring photo
        best_from_each_group = []
        duplicate_count = 0
        
        for group in groups:
            if len(group) > 1:
                duplicate_count += len(group) - 1
                # Sort by score and take the best
                group.sort(key=lambda x: x.get('score', 0), reverse=True)
                best = group[0]
                best['similar_shots'] = len(group)
                best['alternatives'] = [photo['file'] for photo in group[1:]]
                print(f"   ✅ Keeping best: {best['file']} (score: {best['score']}) from {len(group)} similar shots")
            else:
                best = group[0]
                best['similar_shots'] = 1
            
            best_from_each_group.append(best)
        
        # Add back failed photos at the end
        best_from_each_group.extend(failed_results)
        
        print(f"\n📊 Duplicate detection summary:")
        print(f"   • Found {len(groups)} unique shots")
        print(f"   • Removed {duplicate_count} duplicates/similar photos")
        print(f"   • {len(best_from_each_group)} photos remain")
        print(f"   • Made {comparison_count} photo comparisons")
        
        return best_from_each_group
    
    def evaluate_photo(self, image_path):
        """Evaluate a single photo"""
        if not os.path.exists(image_path):
            return None
            
        print(f"Evaluating: {os.path.basename(image_path)}")
        
        if self.use_openai:
            result = self.evaluate_with_openai(image_path)
        else:
            result = self.evaluate_with_ollama(image_path)
        
        result['file'] = os.path.basename(image_path)
        result['path'] = image_path
        return result
    
    def evaluate_folder(self, folder_path, output_file=None):
        """Evaluate all images in a folder"""
        folder = Path(folder_path)
        if not folder.exists():
            print(f"Folder {folder_path} does not exist")
            return []
        
        extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        image_files = [f for f in folder.iterdir() 
                      if f.suffix.lower() in extensions]
        
        if not image_files:
            print(f"No image files found in {folder_path}")
            return []
        
        print(f"Evaluating {len(image_files)} images for social media appeal...")
        if not self.use_openai:
            print("Using Ollama - make sure 'ollama serve' is running and 'llava:latest' is installed")
        
        results = []
        for i, image_file in enumerate(image_files, 1):
            print(f"\nProcessing {i}/{len(image_files)}: {image_file.name}")
            result = self.evaluate_photo(str(image_file))
            if result and result.get('score', 0) > 0:
                results.append(result)
                print(f"  Score: {result['score']}/100")
                if 'reasoning' in result:
                    print(f"  Reason: {result['reasoning']}")
                if 'caption' in result:
                    print(f"  📱 Caption: {result['caption']}")
        
        # Sort by score
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Group similar photos and pick the best from each group
        if self.detect_duplicates:
            results = self.group_similar_photos(results)
            # Re-sort after grouping
            results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {output_file}")
        
        return results
    
    def print_top_results(self, results, top_n=10):
        """Print the top results"""
        if not results:
            print("No results to display")
            return
            
        print(f"\n{'='*80}")
        print(f"TOP {min(top_n, len(results))} PHOTOS FOR SOCIAL MEDIA")
        print(f"{'='*80}")
        
        for i, result in enumerate(results[:top_n], 1):
            print(f"\n{i}. {result['file']}")
            print(f"   Score: {result.get('score', 0)}/100")
            
            # Show duplicate detection info
            if 'similar_shots' in result and result['similar_shots'] > 1:
                print(f"   📎 Best of {result['similar_shots']} similar shots")
                if 'alternatives' in result:
                    alt_list = ', '.join(result['alternatives'][:3])  # Show first 3
                    if len(result['alternatives']) > 3:
                        alt_list += f" (+{len(result['alternatives']) - 3} more)"
                    print(f"      Alternatives: {alt_list}")
            
            if 'main_subject' in result:
                print(f"   Subject: {result['main_subject']}")
            
            if 'reasoning' in result:
                print(f"   Analysis: {result['reasoning']}")
            
            if 'social_media_appeal' in result and result['social_media_appeal'] != result.get('reasoning', ''):
                print(f"   Social Media Appeal: {result['social_media_appeal']}")
            
            if 'caption' in result:
                print(f"   📱 Suggested Caption: {result['caption']}")
            
            if 'improvements' in result:
                print(f"   💡 Improvements: {result['improvements']}")

def main():
    parser = argparse.ArgumentParser(description='AI-powered car photo evaluator with duplicate detection for social media')
    parser.add_argument('folder', help='Folder containing photos to evaluate')
    parser.add_argument('-o', '--output', help='Output JSON file for results')
    parser.add_argument('-c', '--captions', help='Output file for just the captions of top photos')
    parser.add_argument('-n', '--top', type=int, default=10, 
                       help='Number of top photos to display (default: 10)')
    parser.add_argument('--openai-api-key', help='OpenAI API key for GPT-4V (otherwise uses Ollama)')
    parser.add_argument('--no-duplicates', action='store_true', 
                       help='Skip duplicate detection (faster but may include similar shots)')
    
    args = parser.parse_args()
    
    detect_duplicates = not args.no_duplicates
    if detect_duplicates:
        print("🔍 Duplicate detection enabled - will group similar shots and pick the best from each group")
    else:
        print("⚡ Duplicate detection disabled - processing all photos independently")
    
    evaluator = AIPhotoEvaluator(api_key=args.openai_api_key, detect_duplicates=detect_duplicates)
    results = evaluator.evaluate_folder(args.folder, args.output)
    evaluator.print_top_results(results, args.top)
    
    # Save captions separately if requested
    if args.captions and results:
        caption_data = []
        for result in results[:args.top]:
            if 'caption' in result:
                caption_data.append({
                    'file': result['file'],
                    'score': result.get('score', 0),
                    'caption': result['caption']
                })
        
        with open(args.captions, 'w') as f:
            for item in caption_data:
                f.write(f"{item['file']} (Score: {item['score']})\n")
                f.write(f"{item['caption']}\n\n")
        
        print(f"\n📱 Captions saved to {args.captions}")

if __name__ == "__main__":
    main()