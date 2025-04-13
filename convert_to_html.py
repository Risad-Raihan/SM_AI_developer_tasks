import markdown
import os
from pathlib import Path

def convert_md_to_html(markdown_file, output_html):
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Handle images in markdown - convert relative paths to absolute
    base_dir = os.path.dirname(os.path.abspath(markdown_file))
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code']
    )
    
    # Add CSS for better formatting
    html_with_style = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Savory Haven Restaurant Chatbot API Documentation</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2cm; line-height: 1.5; }}
            h1, h2, h3 {{ color: #333; }}
            code {{ background-color: #f5f5f5; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
            pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }}
            img {{ max-width: 100%; height: auto; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Fix image paths in HTML
    for img_path in Path(base_dir).glob('*.png'):
        img_filename = os.path.basename(img_path)
        abs_img_path = os.path.abspath(img_path)
        html_with_style = html_with_style.replace(
            f'src="{img_filename}"', 
            f'src="file:///{abs_img_path.replace(os.sep, "/")}"'
        )
    
    # Save HTML file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_with_style)
    
    print(f"HTML file created: {output_html}")
    print("You can now open this HTML file in a browser and use the browser's Print function to save as PDF.")

if __name__ == "__main__":
    md_file = 'docs/api_documentation.md'
    html_file = 'docs/savory_haven_api_documentation.html'
    convert_md_to_html(md_file, html_file) 