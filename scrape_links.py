import requests
from bs4 import BeautifulSoup
import re
import os

BASE_URL = "https://manvichughwebseries.blogspot.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_all_post_links():
    # Using Blogger feed format to get more post links
    feed_url = f"{BASE_URL}/feeds/posts/default?alt=rss&max-results=500"
    res = requests.get(feed_url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "xml")

    links = []
    for item in soup.find_all("item"):
        link = item.find("link").text
        links.append(link)
    return list(set(links))


def extract_drive_links_from_post(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "drive.google.com" in href:
                links.append(href.strip())
        return links
    except Exception as e:
        print(f"❌ Error parsing {url}: {e}")
        return []


def already_logged_post(url, output_file):
    if not os.path.exists(output_file):
        return False
    with open(output_file, "r", encoding="utf-8") as f:
        return url in f.read()


def main():
    output_file = "output.txt"
    post_urls = get_all_post_links()
    print(f"🔍 Found {len(post_urls)} posts.")

    new_links_found = False

    with open(output_file, "a", encoding="utf-8") as f:
        for i, post_url in enumerate(post_urls, 1):
            if already_logged_post(post_url, output_file):
                print(f"⏩ Skipping already logged post: {post_url}")
                continue

            links = extract_drive_links_from_post(post_url)
            if links:
                print(f"✅ Found {len(links)} link(s) in: {post_url}")
                f.write(f"Post: {post_url}\n")
                for link in links:
                    f.write(f"  - {link}\n")
                f.write("\n")
                new_links_found = True
            else:
                print(f"📭 No links in: {post_url}")

    if new_links_found:
        print("✅ Done! New links saved to output.txt")
    else:
        print("ℹ️ No new links found.")

if __name__ == "__main__":
    main()
