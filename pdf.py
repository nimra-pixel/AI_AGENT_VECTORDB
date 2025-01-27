import requests
from io import BytesIO
import pdfplumber  # For better PDF text extraction
from difflib import get_close_matches


class PDFUrlKnowledgeBase:
    def __init__(self, urls, vector_db=None):
        """Initialize the PDF URL Knowledge Base.

        :param urls: List of PDF URLs
        :param vector_db: A vector database for storing knowledge
        """
        self.urls = urls
        self.vector_db = vector_db
        self.knowledge = []  # Store extracted text from PDFs
        self.dishes = []  # Initialize dishes list
        print("PDFUrlKnowledgeBase initialized with URLs:", urls)

    def load(self, recreate=False, upsert=False):
        """Load knowledge from the given PDFs.

        :param recreate: If True, recreate the knowledge base
        :param upsert: If True, upsert knowledge into the vector DB
        """
        if recreate:
            print("Recreating the knowledge base...")
            if self.vector_db:
                self.vector_db.clear()
            self.knowledge = []
            self.dishes = []  # Reset the dishes list

        for url in self.urls:
            print(f"Processing PDF from URL: {url}")
            try:
                # Download the PDF
                response = requests.get(url)
                response.raise_for_status()
                pdf_content = BytesIO(response.content)

                # Extract text from the PDF using pdfplumber
                pdf_text = self.extract_text_with_pdfplumber(pdf_content)

                # Debug: Save extracted text for verification
                self.save_debug_text(pdf_text, url)

                # Add extracted text to the knowledge base
                self.knowledge.append({"url": url, "content": pdf_text})
                print(f"Successfully processed PDF: {url}")

                # Insert into vector database (optional for advanced search)
                if self.vector_db:
                    self.vector_db.insert(pdf_text, upsert=upsert)

                # Extract and store dish names
                self.extract_dishes(pdf_text)

            except Exception as e:
                print(f"Failed to process PDF at {url}: {e}")

        print("Knowledge base loading complete.")
        print(f"Extracted dishes: {self.dishes}")

    def extract_text_with_pdfplumber(self, pdf_content):
        """Extract text from a PDF using pdfplumber."""
        text = ""
        with pdfplumber.open(pdf_content) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def save_debug_text(self, text, url):
        """Save the extracted text to a file for debugging."""
        file_name = f"debug_extracted_text_{url.split('/')[-1]}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted text saved to {file_name}")

    def extract_dishes(self, text):
        """Extract and store dish names from the text.

        :param text: Full text extracted from the PDF
        """
        potential_dishes = [
            "Pad Thai Goong Sod",
            "Tom Kha Gai",
            "Som Tum",
            "Massaman Gai",
            "Tom Yum Goong",
        ]
        text = text.lower()  # Normalize text to lowercase
        for dish in potential_dishes:
            if dish.lower() in text and dish not in self.dishes:
                self.dishes.append(dish.strip())
                print(f"Dish found and added: {dish.strip()}")

    def search(self, query):
        """Search the knowledge base using the extracted content.

        :param query: Query string
        :return: Search results
        """
        print(f"Searching knowledge base for query: {query}")

        # Special case: list all dishes
        if query.lower() in ["list down all the dishes", "list all the dishes", "show me all dishes"]:
            if self.dishes:
                return [f"- {dish}" for dish in self.dishes]
            else:
                return ["No dishes found in the knowledge base."]

        # General case: search in extracted knowledge
        results = []
        for entry in self.knowledge:
            if query.lower() in entry["content"].lower():
                results.append(f"Match found in PDF from {entry['url']}:")
                snippet = self._get_snippet(entry["content"], query)
                results.append(snippet)
            else:
                # Approximate matching for partial matches
                matches = get_close_matches(query.lower(), entry["content"].lower().split(), n=3, cutoff=0.6)
                if matches:
                    results.append(f"Close match found in PDF from {entry['url']}: {', '.join(matches)}")

        print(f"Search results: {results}")
        return results if results else ["No results found in the knowledge base."]

    def _get_snippet(self, content, query):
        """Get a snippet of text around the query match.

        :param content: Full text content
        :param query: Query string
        :return: Snippet of text
        """
        index = content.lower().find(query.lower())
        if index == -1:
            return "No snippet available."

        start = max(index - 50, 0)
        end = min(index + 50, len(content))
        return content[start:end] + "..."
