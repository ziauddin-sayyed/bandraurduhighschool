
import os
import re

gallery_dir = '/var/www/html/buhs/gallery-media'
html_file = '/var/www/html/buhs/gallery.html'

# Get all media files
media_files = [f for f in os.listdir(gallery_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4'))]
media_files.sort()

# Read HTML
with open(html_file, 'r') as f:
    content = f.read()

# Find existing files in HTML
# Pattern looks for gallery-media/FILENAME in hrefs
existing_files = set(re.findall(r'href="gallery-media/([^"]+)"', content))

# Identiy missing
missing_files = [f for f in media_files if f not in existing_files]

print(f"Found {len(media_files)} total files.")
print(f"Found {len(existing_files)} existing files in HTML.")
print(f"Adding {len(missing_files)} new files.")

new_items_html = ""

for filename in missing_files:
    filepath = f"gallery-media/{filename}"
    is_video = filename.lower().endswith('.mp4')
    
    if is_video:
        item = f'''
<div class="item">
    <a href="{filepath}" data-fancybox="gallery" data-caption="Gallery Video">
        <video preload="none" class="img-fluid img-thumbnail">
            <source src="{filepath}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </a>
</div>'''
    else:
        item = f'''
<div class="item">
    <a href="{filepath}" data-fancybox="gallery" data-caption="Gallery Image"><img data-src="{filepath}" class="owl-lazy img-fluid img-thumbnail" alt="Gallery Image"></a>
</div>'''
    
    new_items_html += item

if new_items_html:
    # Insert before the closing of owl-carousel
    # We look for the closing div followed by container end comment
    # This is susceptible to whitespace changes, but we know the structure from previous edits.
    # Structure:
    # ... items ...
    # </div>
    #         </div><!-- end container -->
    
    target = '</div>\n        </div><!-- end container -->'
    replacement = f'{new_items_html}\n</div>\n        </div><!-- end container -->'
    
    if target in content:
        content = content.replace(target, replacement)
        with open(html_file, 'w') as f:
            f.write(content)
        print("Successfully added new items to gallery.html")
    else:
        print("Error: Could not find insertion point in gallery.html")
        # Fallback debug
        print("Tail of content:")
        print(content[-500:])
else:
    print("No new files to add.")
