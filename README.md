# PDF Assistant

This project implements a PDF-based knowledge assistant using Python. The assistant reads content from a PDF hosted online, processes it, stores the extracted knowledge, and allows interactive querying through a CLI.

---

## Features

- Extracts text content from PDF files hosted online.
- Supports knowledge base creation and search functionality.
- Stores and retrieves knowledge in/from a vector database (optional).
- Lists extracted dishes or relevant content interactively.
- CLI-based interaction for querying the knowledge base.

---

## Prerequisites

Ensure the following are installed on your system:

- Python 3.8 or higher
- `pip` for managing Python packages

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/pdf-assistant.git
   cd pdf-assistant
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Edit the `pdf_assistant.py` file to include the desired PDF URL:
   ```python
   urls = ["https://example.com/path/to/your.pdf"]
   ```

2. Run the script:
   ```bash
   python pdf_assistant.py
   ```

3. Interact with the assistant through the CLI:
   - List all dishes:
     ```
     > list all the dishes
     ```
   - Search for specific content:
     ```
     > what are the ingredients of Massaman Gai?
     ```
   - Exit the CLI:
     ```
     > exit
     ```

---

## Project Structure

- `pdf_assistant.py` - Main script to run the assistant.
- `pdf.py` - Module for handling PDF text extraction and knowledge base creation.
- `README.md` - Project documentation.

---

## Dependencies

The project requires the following Python libraries:

- `requests` - For downloading PDFs from URLs.
- `pdfplumber` - For extracting text from PDF files.
- `difflib` - For approximate text matching.
- `PyPDF2` - For basic PDF processing (optional, backup for `pdfplumber`).

To install these dependencies, use:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Common Issues

1. **PDF content not found**:
   - Ensure the PDF URL is accessible.
   - Use `pdfplumber` for better text extraction.

2. **Empty search results**:
   - Verify the PDF content contains the query text.
   - Check if the text extraction was successful (debugging logs in the terminal).

3. **Assistant CLI not interactive**:
   - Confirm the `Assistant` class parameters match the library’s requirements.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request on GitHub.

---

 
