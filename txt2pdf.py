#!/usr/bin/env python3

import os
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def txt_to_pdf(input_file, output_file=None):
    """
    Convert a .txt file to a PDF using reportlab.
    
    Args:
        input_file (str): Path to the input .txt file.
        output_file (str, optional): Path to the output PDF file. If not provided, it will be generated from the input file name.
    """
    # Generate output file name if not provided
    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + ".pdf"
    else:
        # Ensure the output file has a .pdf extension
        if not output_file.endswith('.pdf'):
            output_file += ".pdf"

    # Set up the canvas and document
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    margin = 40
    x = margin
    y = height - margin  # Start from the top of the page

    max_width = width - 2 * margin  # Available text width
    line_height = 14  # Line height for text

    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:  # Skip empty lines
                # Wrap the text to fit within the page width
                wrapped_lines = simpleSplit(line, "Helvetica", 12, max_width)
                for wrapped_line in wrapped_lines:
                    if y - line_height < margin:  # Check for page overflow
                        c.showPage()  # Add a new page
                        y = height - margin  # Reset the y-coordinate
                    c.drawString(x, y, wrapped_line)
                    y -= line_height

    # Save the PDF
    c.save()
    print(f"PDF generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a .txt file to a .pdf file.")
    parser.add_argument("input_file", help="The input .txt file to convert.")
    parser.add_argument("-o", "--output", help="The output PDF file name (optional).")

    args = parser.parse_args()

    # Convert TXT to PDF
    txt_to_pdf(args.input_file, args.output)
