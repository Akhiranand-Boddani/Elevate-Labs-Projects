import requests
import os

def test_extraction():
    url = "http://localhost:8000/api/extract-text"
    
    # Create a dummy text file
    with open("test_upload.txt", "w") as f:
        f.write("This is some test content for the extraction endpoint. It should be able to read this and return it as text.")
    
    try:
        with open("test_upload.txt", "rb") as f:
            files = {"file": ("test_upload.txt", f, "text/plain")}
            response = requests.post(url, files=files)
            
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Extraction test: PASSED")
        else:
            print("❌ Extraction test: FAILED")
            
    except Exception as e:
        print(f"❌ Extraction test: ERROR ({e})")
    finally:
        if os.path.exists("test_upload.txt"):
            os.remove("test_upload.txt")

if __name__ == "__main__":
    test_extraction()
