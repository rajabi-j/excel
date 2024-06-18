from flask import Flask, request, send_file
import pandas as pd
import tempfile
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_files():
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False) as temp_file1, tempfile.NamedTemporaryFile(delete=False) as temp_file2:
        temp_file1.write(file1.read())
        temp_file2.write(file2.read())
        temp_file1_path = temp_file1.name
        temp_file2_path = temp_file2.name

    # Process the files
    result_file_path = process_files(temp_file1_path, temp_file2_path)

    # Clean up temporary files
    os.remove(temp_file1_path)
    os.remove(temp_file2_path)

    return send_file(result_file_path, as_attachment=True)

def process_files(file1_path, file2_path):
    # Your processing code here
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)
    
    # Perform processing and save the result
    result_df = df1.merge(df2, on='common_column')  # Example merge
    result_file = tempfile.NamedTemporaryFile(delete=False)
    result_file_path = result_file.name
    result_df.to_excel(result_file_path, index=False)
    
    return result_file_path

if __name__ == '__main__':
    app.run(debug=True)
