import os
import glob
import re

template_dir = r"c:\project\portofolio\curhatbox\main\templates\**\*.html"
files = glob.glob(template_dir, recursive=True)

# Replacements for Bootstrap 5.3 Theme Support
replacements = [
    (r'\btext-dark\b', 'text-body'),
    (r'\bbg-white\b', 'bg-body'),
    (r'\bbg-light\b', 'bg-body-tertiary'),
    (r'\btext-muted\b', 'text-body-secondary'), # Better contrast in dark mode
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for old, new in replacements:
        content = re.sub(old, new, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")
print("Theme class replacement complete.")
