from tika import parser

def tikaTextExtractor(file_path):
    print("Extracting text from file: " + file_path)
    parsed_tika=parser.from_file(file_path)
    return parsed_tika["content"]