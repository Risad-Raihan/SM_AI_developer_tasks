import markdown
import os
import pdfkit
from pathlib import Path

def convert_md_to_pdf(markdown_file, output_pdf):
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Handle images in markdown - convert relative paths to absolute
    base_dir = os.path.dirname(os.path.abspath(markdown_file))
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    # Add CSS for better formatting
    html_with_style = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
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
    
    # Save HTML to a temporary file
    temp_html = os.path.join(os.path.dirname(output_pdf), 'temp.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_with_style)
    
    try:
        # Try to use pdfkit to convert HTML to PDF
        # Note: This requires wkhtmltopdf to be installed on the system
        pdfkit.from_file(temp_html, output_pdf)
        print(f"PDF created: {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure wkhtmltopdf is installed and available in PATH.")
        print("You can download it from: https://wkhtmltopdf.org/downloads.html")
    
    # Clean up the temporary HTML file
    if os.path.exists(temp_html):
        os.remove(temp_html)

if __name__ == "__main__":
    md_file = 'docs/api_documentation.md'
    pdf_file = 'docs/savory_haven_api_documentation.pdf'
    convert_md_to_pdf(md_file, pdf_file) 