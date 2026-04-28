"""
Factory Method:


"""


# Document Export System
"""
Document export system:
 -> generate report in multiple formats
"""


from abc import ABC, abstractmethod

class Document(ABC):

    @abstractmethod
    def get_header(self) -> str:
        pass

    @abstractmethod
    def format_raw(self, data: list[str]) -> str:
        pass


    @abstractmethod
    def get_footer(self) -> str:
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        pass

# concrete product
# Concrete Products
class PdfDocument(Document):
    def get_header(self) -> str:
        return "--- PDF DOCUMENT START ---"

    def format_row(self, data: list[str]) -> str:
        return "| " + " | ".join(data) + " |"

    def get_footer(self) -> str:
        return "--- PDF DOCUMENT END ---"

    def get_file_extension(self) -> str:
        return ".pdf"

class HtmlDocument(Document):
    def get_header(self) -> str:
        return "<html><body><table>"

    def format_row(self, data: list[str]) -> str:
        cells = "".join(f"<td>{cell}</td>" for cell in data)
        return f"<tr>{cells}</tr>"

    def get_footer(self) -> str:
        return "</table></body></html>"

    def get_file_extension(self) -> str:
        return ".html"

class CsvDocument(Document):
    def get_header(self) -> str:
        return ""

    def format_row(self, data: list[str]) -> str:
        return ",".join(data)

    def get_footer(self) -> str:
        return ""

    def get_file_extension(self) -> str:
        return ".csv"


# Abstract Creator
class ExportCreator(ABC):
    @abstractmethod
    def create_document(self) -> Document:
        pass

    def export(self, data: list[list[str]]) -> None:
        doc = self.create_document()
        print(f"Exporting to {doc.get_file_extension()} format...")

        header = doc.get_header()
        if header:
            print(header)

        for row in data:
            print(doc.format_row(row))

        footer = doc.get_footer()
        if footer:
            print(footer)

        print("Export complete.\n")


# Concrete Creators
class PdfExportCreator(ExportCreator):
    def create_document(self) -> Document:
        return PdfDocument()

class HtmlExportCreator(ExportCreator):
    def create_document(self) -> Document:
        return HtmlDocument()

class CsvExportCreator(ExportCreator):
    def create_document(self) -> Document:
        return CsvDocument()


report_data = [
        ["Name", "Department", "Salary"],
        ["Alice", "Engineering", "120000"],
        ["Bob", "Marketing", "95000"],
        ["Charlie", "Design", "105000"],
    ]

pdf_exporter = PdfExportCreator()
pdf_exporter.export(report_data)

html_exporter = HtmlExportCreator()
html_exporter.export(report_data)

csv_exporter = CsvExportCreator()
csv_exporter.export(report_data)