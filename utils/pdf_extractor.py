import pathlib
from utils.logger import logger

# Cache for extracted PDF text to avoid repeated extraction
_pdf_text_cache = {}

def extract_text_from_pdf(pdf_path: str) -> str | None:
    """
    Extract text content from a PDF file.
    Uses PyMuPDF (fitz) if available, otherwise falls back to basic extraction.
    Results are cached to avoid repeated extraction.
    """
    try:
        # Return cached result if available
        if pdf_path in _pdf_text_cache:
            logger.info(f"Using cached PDF text for: {pdf_path}")
            return _pdf_text_cache[pdf_path]
        
        filepath = pathlib.Path(pdf_path)
        if not filepath.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            return None
        
        text = ""
        
        # Try PyMuPDF (fitz) first - best quality
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
            logger.info(f"Extracted PDF text using PyMuPDF: {len(text)} characters")
        except ImportError:
            # Fallback to pypdf if fitz not available
            try:
                from pypdf import PdfReader
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                logger.info(f"Extracted PDF text using pypdf: {len(text)} characters")
            except ImportError:
                logger.error("No PDF extraction library available. Install PyMuPDF or pypdf.")
                return None
        
        if not text.strip():
            logger.warning("No text extracted from PDF")
            return None
        
        # Cache the result
        _pdf_text_cache[pdf_path] = text.strip()
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return None
