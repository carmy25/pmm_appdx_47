import os
import sys
from pdf2image import convert_from_path
from PIL import Image

def convert_pdfs_to_jpegs(pdf_dir, output_dir, dpi=300):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through all PDF files in the directory
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            try:
                # Convert the first page of the PDF to an image
                images = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=1)

                if images:
                    # Define output image path
                    output_filename = os.path.splitext(filename)[0] + ".jpg"
                    output_path = os.path.join(output_dir, output_filename)

                    # Save the first page as JPEG
                    images[0].save(output_path, "JPEG")
                    print(f"Saved: {output_path}")
                else:
                    print(f"Skipping {filename}: No pages found.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage
if __name__ == "__main__":
    breakpoint()
    input_directory = sys.argv[1]  # Change this to the folder containing PDFs
    output_directory = sys.argv[2]  # Change this to where you want to save JPEGs
    
    convert_pdfs_to_jpegs(input_directory, output_directory)
