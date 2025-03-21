import pymupdf  # import the bindings
from PIL import Image
import google.generativeai as genai
import os
import dotenv
import re
import json

# Load environment variables
#otenv.load_dotenv()
fname = "input.pdf"  # get filename from command line
doc = pymupdf.open(fname)  # open document
for page in doc:  # iterate through the pages
    pix = page.get_pixmap(dpi=300)  # render page to an image
    pix.save("images/page-%i.png" % page.number)  # store image as a PNG in the images folder
def extract_page_number(filename):
    """Extracts the numeric part of the filename safely using regex."""
    match = re.search(r"(\d+)", filename)
    return int(match.group()) if match else float("inf")  # Assign large value if no number found
def ocr_with_gemini(image_paths,prompt = "Hi", model_name="gemini-2.0-flash-lite"):
    """Process images with Gemini 2.0 Flash for OCR"""
    images = [Image.open(path) for path in image_paths]
    
    # Initialize the model (assuming you've set up your API key)
    model = genai.GenerativeModel(model_name=model_name)
        
    try:
        response = model.generate_content([prompt, *images])
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle potential errors gracefully
        return None
# Function to read OCR data from a JSON file
# Function to read OCR data from a JSON file
def read_ocr_data(file_path):
    try:
        with open(file_path, 'r') as f:
            ocr_data = json.load(f)
        return ocr_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# ✅ Function to generate RFQ (Request for Quotation)

# Define the folder containing the images
image_folder = "images"

# Get the list of image paths from the folder
image_paths = sorted(
    [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(".png")],
    key=lambda x: extract_page_number(os.path.basename(x))  # Sort by extracted number
)

# Set your API key.  This *must* be done before calling the function.
# Replace "YOUR_API_KEY" with your actual API key.
genai.configure(api_key="AIzaSyArI4YW8bukyj2z-UYpo46iBhkoecvWPWM")


#genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
prompt = """
Extract key details from a technical drawing image and present them in a structured json format.
Do not include any irrelevant information. If any details are unclear or missing, mark them as such.
### **Details to Extract:**  
1. **Title / Part Name**  
2. **Drawing Number**  
3. **Material**  
4. **Key Dimensions & Tolerances**  
   - Overall dimensions (Length, Width, Thickness)  
   - Hole sizes & positions  
   - Tolerances specified  
5. **Surface Finish & Processing Notes**  
6. **Scale & Revision**  
7. **Author, Checker, & Approval Info**  
8. **Other Notes**  
Incase you find any extra attributes, please include them as well.
### **Output Format (Example):**  
{
    "Title": "",
    "Drawing Number": "",
    "Material": "",
    "Dimensions": [
        {
            "Length": " mm"
        },
        {
            "Width": " mm"
        },
        {
            "Thickness": " mm"
        },
        {
            "Hole Diameter": " mm (through)"
        },
        {
            "Hole Spacing": " mm"
        },
        {
            "Edge Offset": " mm"
        }
    ],
    "Tolerances": [
        {
            "Length": " mm"
        },
        {
            "Width": " mm"
        },
        {
            "Hole Position": " mm"
        }
    ],
    "Surface Finish": "DEBURR & BLACKEN",
    "Hardness": "Toughened to  Kgf/mm²",
    "Scale": "",
    "Revision": "",
    "Drawn By": "",
    "Checked By": "",
    "Approved By": "",
    "Date": "",
     "Model Weight": ""
    "Other Notes": "Replacement for / by"
}

### **Instructions:**  
- Prioritize text from the title block and annotations.  
- Maintain accuracy in extracted dimensions and tolerances.  
- Output in structured json format for easy redability.
- save the final output in json format as a json file named Ocr_output.json
"""
Extracted_Ocr_data=ocr_with_gemini(image_paths, prompt=prompt)

if Extracted_Ocr_data:
    print(Extracted_Ocr_data)
if Extracted_Ocr_data:
    # Save the raw OCR data as a text file
    with open("ocr_data.json") as text_file:
        json.dump(Extracted_Ocr_data,text_file)
    # print("OCR data saved to ocr_data.txt")
from cost_estimation import create_parts_csv, create_machine_csv, create_process_csv, calculate_total_cost


