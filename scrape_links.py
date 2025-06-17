import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://manvichughwebseries.blogspot.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_all_post_links():
    page = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    post_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/202" in href and href.startswith("https://"):
            post_links.append(href)

    return list(set(post_links))  # remove duplicates


def extract_drive_links_from_post(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        all_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "drive.google.com" in href:
                all_links.append(href)

        return all_links
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return []


def main():
    post_urls = get_all_post_links()
    print(f"Found {len(post_urls)} posts.")

    with open("output.txt", "w", encoding="utf-8") as f:
        for i, post_url in enumerate(post_urls, 1):
            drive_links = extract_drive_links_from_post(post_url)
            if drive_links:
                f.write(f"Post {i}: {post_url}\n")
                for link in drive_links:
                    f.write(f"  - {link}\n")
                f.write("\n")

    print("✅ All drive links saved to output.txt")

if __name__ == "__main__":
    main()
