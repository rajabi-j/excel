from flask import Flask, request, jsonify, send_file
import pandas as pd  
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_files():
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Save files to a temporary directory
    file1.save(os.path.join('temp', file1.filename))
    file2.save(os.path.join('temp', file2.filename))
    
    # Process the files 
    result_file_path = process_files(file1.filename, file2.filename)
    
    return send_file(result_file_path, as_attachment=True)

def process_files(file1, file2):
    df1 = pd.read_excel(os.path.join('temp', file1))
    df2 = pd.read_excel(os.path.join('temp', file2))
    
    # Perform processing and save the result
    result_df = df1.merge(df2, on='common_column')  # Example merge
    result_file_path = os.path.join('temp', 'result.xlsx')
    result_df.to_excel(result_file_path, index=False)
    
    return result_file_path

if __name__ == '__main__':
    app.run(debug=True)
