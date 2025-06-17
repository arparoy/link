import hashlib

LINK_FILE = 'link.txt'
OUTPUT_FILE = 'links.md'
HASH_FILE = '.link_hash'

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
        f.write("| Serial Number | Link |\n")
        f.write("|---------------|------|\n")
        for i, link in enumerate(links, 1):
            f.write(f"| {i} | [Click here]({link}) |\n")

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
