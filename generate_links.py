import hashlib
import re

LINK_FILE = 'link.txt'
OUTPUT_FILE = 'links.md'
HASH_FILE = '.link_hash'

PLATFORM_PATTERNS = {
    "YouTube": r"(youtube\.com|youtu\.be)",
    "Facebook": r"facebook\.com",
    "Google Drive": r"drive\.google\.com",
    "Google Photos": r"photos\.google\.com",
    "Terabox": r"terabox\.com",
    "OneDrive": r"1drv\.ms|onedrive\.live\.com",
    "Mega": r"mega\.nz",
    "Dropbox": r"dropbox\.com",
    "Proton Drive": r"proton\.me|protondrive\.com",
    "Blog": r"\.blogspot\.com|\.wordpress\.com",
    "Instagram": r"instagram\.com",
    "TikTok": r"tiktok\.com",
    "Twitter": r"twitter\.com|x\.com",
    "Telegram": r"t\.me",
}

def detect_platform(link):
    for platform, pattern in PLATFORM_PATTERNS.items():
        if re.search(pattern, link, re.IGNORECASE):
            return platform
    return "Other"

def hash_links(links):
    return hashlib.sha256("".join(links).encode()).hexdigest()

def read_links():
    with open(LINK_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def read_existing_hash():
    try:
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''

def save_hash(new_hash):
    with open(HASH_FILE, 'w') as f:
        f.write(new_hash)

def generate_md(links):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Links Table\n\n")
        f.write("| Serial Number | Link | Platform |\n")
        f.write("|---------------|------|----------|\n")
        for i, link in enumerate(links, 1):
            platform = detect_platform(link)
            f.write(f"| {i} | [Click here]({link}) | {platform} |\n")

def main():
    links = read_links()
    new_hash = hash_links(links)
    old_hash = read_existing_hash()

    if new_hash != old_hash:
        generate_md(links)
        save_hash(new_hash)
        print("✅ Updated links.md with new links.")
        return True
    else:
        print("🔁 No new links. Skipping update.")
        return False

if __name__ == "__main__":
    main()
