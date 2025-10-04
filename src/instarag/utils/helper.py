import mimetypes


def get_content_type(filepath: str) -> str:
    """
    Determine the content type of the file using its extension and inspection.
    """
    # Determine MIME type by file name extension
    mimetype_by_name, _ = mimetypes.guess_type(filepath)

    # Fallback: Inspect the file's content (basic heuristic)
    def inspect_file_content(file_path: str) -> str:
        with open(file_path, "rb") as file:
            header = file.read(512)  # Read the first 512 bytes for inspection
        if b"%PDF-" in header:
            return "application/pdf"
        elif b"PK" in header and b"[Content_Types].xml" in header:
            return "application/vnd.openxmlformats-officedocument"
        elif b"<!DOCTYPE html>" in header or b"<html>" in header:
            return "text/html"
        elif b"," in header or b";" in header:
            return "text/csv"
        elif b"\t" in header:
            return "text/tsv"
        else:
            return "application/octet-stream"  # Default binary type

    # Return MIME type by name or inspect the file content as a fallback
    return mimetype_by_name or inspect_file_content(filepath)