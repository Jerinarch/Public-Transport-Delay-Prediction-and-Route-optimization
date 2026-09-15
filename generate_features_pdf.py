import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_dataset_report_pdf import generate_pdf_document

if __name__ == "__main__":
    md_filepath = r"d:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\App_and_Software_Features_Design_Specification.md"
    pdf_filepath = r"d:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\App_and_Software_Features_Design_Specification.pdf"
    generate_pdf_document(md_filepath, pdf_filepath)
