from datetime import datetime

def convert_md_table_to_html(md_file, html_file, css_path="style.css", github_user="arparoy"):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    table_lines = [line.strip() for line in lines if "|" in line]
    if not table_lines or len(table_lines) < 3:
        print("❌ No valid Markdown table found.")
        return

    headers = [h.strip() for h in table_lines[0].split("|")[1:-1]]
    rows = [line.split("|")[1:-1] for line in table_lines[2:]]

    platform_icons = {
        "YouTube": "🎥", "Facebook": "📘", "Google Drive": "📁", "Google Photos": "🖼️",
        "Terabox": "📦", "OneDrive": "☁️", "Mega": "🧰", "Dropbox": "🗃️", "Porton Drive": "🔒",
        "Blogs": "📝", "Sites": "🌐", "GitHub": "🐙"
    }

    def parse_cell(cell, header):
        cell = cell.strip()
        if header.lower() == "link" and "[Click here]" in cell and "](" in cell:
            try:
                url = cell.split("](")[1].split(")")[0]
                return f'<a href="{url}" target="_blank">Click here</a>'
            except:
                return cell
        elif header.lower() == "platform":
            icon = platform_icons.get(cell, "🔗")
            return f"{icon} {cell}"
        else:
            return cell

    last_updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Link Table</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <h1>Useful Links</h1>
    <input type="text" id="searchInput" placeholder="Search by platform or keyword..." onkeyup="searchTable()" />

    <table id="linkTable">
        <thead>
            <tr>
                {''.join(f"<th>{header}</th>" for header in headers)}
            </tr>
        </thead>
        <tbody>
            {''.join(
                "<tr>" +
                ''.join(f'<td data-label="{headers[i]}">{parse_cell(cell, headers[i])}</td>' for i, cell in enumerate(row)) +
                "</tr>" for row in rows
            )}
        </tbody>
    </table>

    <footer>
        <p>Made with ❤️ by <a href="https://github.com/{github_user}" target="_blank">@{github_user}</a></p>
        <p>Last updated: {last_updated}</p>
    </footer>

    <script>
        function searchTable() {{
            const input = document.getElementById("searchInput");
            const filter = input.value.toLowerCase();
            const rows = document.querySelectorAll("#linkTable tbody tr");
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? "" : "none";
            }});
        }}
    </script>
</body>
</html>
"""
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ HTML table written to {html_file}")

if __name__ == "__main__":
    convert_md_table_to_html("links.md", "index.html")
