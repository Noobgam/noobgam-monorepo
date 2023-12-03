from tika import parser

if __name__ == "__main__":
    raw = parser.from_file("some_pdf.pdf")
    print(raw["content"])
