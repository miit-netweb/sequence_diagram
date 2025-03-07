import ast
import google.generativeai as genai
import os
import sys
from gemini import call_bot
from flask import Flask, request, jsonify,send_file
import json
from flask_cors import CORS  # Import CORS


app = Flask(__name__, static_url_path='/static')

CORS(app, resources={
    "/preparepriorities": {
        "origins": "*",  # Allow all origins (replace with your frontend URL in production)
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
 
mainPrompt = ""

# Configure your API key
GOOGLE_API_KEY = "AIzaSyDrJI0ewPGZzsPRW8Dcy9qBMO_gMxLfIVc" 
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    sys.exit(1)
 
genai.configure(api_key=GOOGLE_API_KEY)
 
def generate_paraphrase_from_code(prompt_or_code):
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Instructions:
    You are tasked with analyzing the provided code snippet and paraphrasing it into a structured description of interactions between components. Your output should focus on the sequence of operations, method calls, and object interactions. This description will later be used to generate a sequence diagram.

    Identify Key Components :
    1. List all classes, functions, or modules involved in the code.
    2. Identify any external systems, APIs, or databases being interacted with.
    Describe Interactions :
    1. For each interaction, describe who initiates the call and what is being called.
    2. Include details about parameters passed and return values (if relevant).
    3. Highlight the order of operations.
    Paraphrase for Sequence Diagram Generation :
    1. Use clear, concise language to describe the flow of execution.
    2. Format the output as a step-by-step narrative or bullet points.
    3. Ensure the description is abstract enough to be visualized as a sequence diagram but detailed enough to capture the essence of the interactions.
    
    Example Output Format :
    
    1. Component A calls Method X in Component B with parameter P1.
    2. Component B processes P1 and calls Method Y in Component C.
    3. Component C interacts with External API D to fetch data.
    4. Component C returns the fetched data to Component B.
    5. Component B processes the data and returns the result to Component A.
    
    The output should be as concise as possible. try to make it as short as short
    
    Here I am providing the code to convert as per the above instruction:
    {prompt_or_code}

    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating sequence diagram: {e}")
        return None
    
def recursively_read_files(folder_path):
    """Recursively reads all files in a folder and its subfolders."""
    global mainPrompt
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                # It's a file
                try:
                    with open(item_path, 'r', encoding='utf-8') as file: #added encoding to handle various file types.
                        content = file.read()
                        mainPrompt += content
                        mainPrompt +="\n"
                except UnicodeDecodeError:
                    print(f"Skipping binary file or file with unknown encoding: {item_path}")
                except Exception as e:
                    print(f"Error reading file {item_path}: {e}")
            elif os.path.isdir(item_path):
                # It's a subfolder
                recursively_read_files(item_path)
    except FileNotFoundError:
        print(f"Error: Folder not found: {folder_path}")
    except PermissionError:
        print(f"Error: Permission denied for folder: {folder_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
@app.route('/preparepriorities', methods=['POST'])
def CallApi():
    promptString = ""
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('files')
    for file in files:
        original_name = file.filename
        content_bytes = file.read()  # b'const express = require(...);'
        # 4. Get content as text (decode bytes)
        content_text = content_bytes.decode('utf-8')
        promptString += original_name
        promptString += "\n"
        promptString += content_text
        promptString += "\n"
    try:
        call_bot(promptString)
        image_path = "D:\AI\sequence_diagram\sequence_diagram.png"
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        return send_file(
            image_path,
            mimetype='image/png',  # Adjust based on actual image type
            as_attachment=False,
            download_name='output.png'
        )
    except Exception as e:
        return jsonify({'error': e}), 400


if __name__ == "__main__":
    app.run(debug=True,port=5006,use_reloader=False)
    # main_folder = "project"  # Replace with your folder path
    # recursively_read_files(main_folder)
    
    # # This line paraphrases the code
    # # output = generate_paraphrase_from_code(mainPrompt)
    
    # call_bot(mainPrompt)
    

