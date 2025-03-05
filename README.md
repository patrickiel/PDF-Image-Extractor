# PDF Image Extractor

A Python tool to extract images from PDF files with intelligent filtering and organization.

## Features

- 📄 Extract images from PDF files
- 📁 Organized output structure
- 🖼️ Preserve original image formats
- 🔍 Filter out small images and duplicates
- 🛠️ Simple command-line interface

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Unix/MacOS
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

1. Place your PDF files in the `pdfs` directory
2. Run the script:
   ```bash
   python pdf-image-extractor.py
   ```
3. Extracted images will be saved in the `extracted_images` directory

### Advanced Options

```bash
python pdf-image-extractor.py [INPUT_DIR] [--output_dir OUTPUT_DIR] [--min_size MIN_SIZE]
```

#### Arguments:
- `INPUT_DIR`: Directory containing PDF files (optional, default: ./pdfs)
- `--output_dir`: Directory to save extracted images (default: ./extracted_images)
- `--min_size`: Minimum pixel dimension for images (default: 100)

#### Examples:
```bash
# Use default pdfs directory
python pdf-image-extractor.py

# Specify custom input directory
python pdf-image-extractor.py my_pdfs

# Extract images with custom minimum size
python pdf-image-extractor.py --min_size 200

# Specify custom input and output directories
python pdf-image-extractor.py my_pdfs --output_dir my_images
```

## Directory Structure

```
.
├── pdfs/                  # Place your PDF files here
├── extracted_images/     # Contains extracted images
│   └── pdf_name/        # Subdirectory for each PDF
│       └── pageX_imgY_WxH.ext  # Extracted images
├── pdf-image-extractor.py
├── requirements.txt
└── README.md
```

## Output Format

Extracted images are named using the following format:
```
page{page_number}_img{image_index}_{width}x{height}.{extension}
```

Example: `page1_img0_800x600.jpg`

## Notes

- Each PDF's images are extracted to a separate subdirectory
- Small images and duplicates are automatically filtered
- Original image formats are preserved

## Troubleshooting

1. **No PDFs found**: Ensure your PDF files are in the specified input directory
2. **Permission errors**: Check write permissions for output directory
3. **Corrupted PDFs**: The script will skip problematic pages and continue processing
4. **Memory issues**: Process large PDFs one at a time

## License

This project is licensed under the MIT License - see the LICENSE file for details. 