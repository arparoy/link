import os

def convert_md_table_to_html(md_file, html_file, css_path="style.css"):
    # Read the Markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract lines containing table data
    table_lines = [line.strip() for line in lines if "|" in line]
    if not table_lines or len(table_lines) < 3:
        print("❌ No valid Markdown table found.")
        return

    # Parse headers and rows
    headers = [h.strip() for h in table_lines[0].split("|")[1:-1]]
    rows = [line.split("|")[1:-1] for line in table_lines[2:]]

    # Build the HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Link Table</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <h1>Links Table</h1>
    <table>
        <thead>
            <tr>
                {''.join(f"<th>{header}</th>" for header in headers)}
            </tr>
        </thead>
        <tbody>
            {''.join(
                "<tr>" +
                ''.join(f'<td data-label="{headers[i]}">{cell.strip()}</td>' for i, cell in enumerate(row)) +
                "</tr>" for row in rows
            )}
        </tbody>
    </table>
</body>
</html>
"""

    # Write the HTML output
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML table written to {html_file}")

if __name__ == "__main__":
    convert_md_table_to_html("links.md", "links.html")
