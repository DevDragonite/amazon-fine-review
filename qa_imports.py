import datetime
import traceback

def test_imports():
    packages = [
        "pandas",
        "numpy",
        "plotly",
        "streamlit",
        "sklearn",
        "nltk",
        "spacy",
        "textblob",
        "vaderSentiment",
        "langdetect",
        "openpyxl",
        "scipy",
        "networkx",
        "sqlite3"
    ]
    
    success = True
    log_file = "output/nlp_qa_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\\n--- PASO 0 QA: {timestamp} ---\\n")
        
        for pkg in packages:
            try:
                __import__(pkg)
                f.write(f"[OK] {pkg} imported successfully.\\n")
            except ImportError as e:
                f.write(f"[ERROR] Failed to import {pkg}: {e}\\n")
                f.write(traceback.format_exc())
                success = False
                
        try:
            import spacy
            spacy.load("en_core_web_sm")
            f.write("[OK] spacy en_core_web_sm model loaded successfully.\\n")
        except Exception as e:
            f.write(f"[ERROR] Failed to load spacy en_core_web_sm model: {e}\\n")
            f.write(traceback.format_exc())
            success = False

    return success

if __name__ == "__main__":
    if test_imports():
        print("All imports passed.")
    else:
        print("Some imports failed. Check output/nlp_qa_log.txt")
        exit(1)
