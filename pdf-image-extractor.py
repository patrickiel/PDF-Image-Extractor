import os
import argparse
import fitz  # PyMuPDF
from PIL import Image
import io
import hashlib
from tqdm import tqdm

def extract_images_from_pdf(pdf_path, output_dir, min_size=100):
    """
    Extract all images from a PDF file and save them to the output directory.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images
        min_size: Minimum pixel size for images to extract (filters out tiny images)
    """
    # Create a unique subfolder for this PDF to avoid name conflicts
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_dir = os.path.join(output_dir, pdf_name)
    os.makedirs(pdf_output_dir, exist_ok=True)
    
    print(f"\nProcessing: {pdf_path}")
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    image_count = 0
    extracted_images = set()  # Track image hashes to avoid duplicates
    
    # Create progress bar for pages
    pbar = tqdm(total=len(doc), desc="Extracting images", unit="page")
    
    # Iterate through each page
    for page_num, page in enumerate(doc):
        # Get all images on the page
        image_list = page.get_images(full=True)
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]  # Image reference number
            
            # Extract the image data
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Generate hash to identify duplicate images
            img_hash = hashlib.md5(image_bytes).hexdigest()
            if img_hash in extracted_images:
                continue
                
            extracted_images.add(img_hash)
            
            # Try to identify the image type
            image_ext = base_image["ext"]
            
            # Load image with PIL to verify it's valid and check dimensions
            try:
                img = Image.open(io.BytesIO(image_bytes))
                width, height = img.size
                
                # Skip small images (often icons, bullets, etc.)
                if width < min_size or height < min_size:
                    continue
                    
                # Save the image
                image_count += 1
                img_filename = f"page{page_num+1}_img{img_index}_{width}x{height}.{image_ext}"
                img_path = os.path.join(pdf_output_dir, img_filename)
                
                with open(img_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                pbar.set_postfix({"images": image_count})
                
            except Exception as e:
                print(f"\nError extracting image: {e}")
        
        pbar.update(1)
    
    pbar.close()
    print(f"Extracted {image_count} unique images from {pdf_path}")
    return image_count

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Extract images from all PDFs in a directory')
    parser.add_argument('input_dir', help='Directory containing PDF files')
    parser.add_argument('--output_dir', help='Directory to save extracted images (default: ./extracted_images)', 
                      default='./extracted_images')
    parser.add_argument('--min_size', type=int, help='Minimum pixel dimension for images (default: 100)', 
                      default=100)
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Find PDF files recursively
    pdf_files = []
    for root, _, files in os.walk(args.input_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    if not pdf_files:
        print(f"No PDF files found in {args.input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Process each PDF with progress bar
    total_images = 0
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs", unit="pdf"):
        image_count = extract_images_from_pdf(pdf_path, args.output_dir, args.min_size)
        total_images += image_count
    
    print(f"\nTotal images extracted: {total_images}")

if __name__ == "__main__":
    main()
