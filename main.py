from flask import Flask, make_response, request
import csv

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("-", ",")


@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Upload your csv file</h1>

                <form action="/hash" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/hash', methods=["POST"])
def hash_data():
    file = request.files['data_file']
    if not file:
        return "No file"

    file_contents = file.stream.read().decode("utf-8")
    csv_input = csv.reader(file_contents)
    print(file_contents)
    print(type(file_contents))
    print(csv_input)
    for row in csv_input:
        print(row)

    result = transform(file_contents)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)