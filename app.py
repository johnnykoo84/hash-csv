from flask import Flask, make_response, request
import csv
import pandas as pd
import hashlib
import io

app = Flask(__name__)

def hash_csv(csv_file):
    # return text_file_contents.replace("-", ",")
    # reading CSV input
    # df = pd.read_csv('student.csv')
    print('print file', csv_file)

    df = pd.read_csv(csv_file)

    print('!!!!!!!df here', df)
    # hashing the 'Password' column
    df['name'] = df['name'].apply(lambda x: \
            hashlib.sha256(x.encode('utf-8')).hexdigest())

    df['mobile'] = df['mobile'].apply(lambda x: \
            hashlib.sha256(x.encode('utf-8')).hexdigest())

    df['email'] = df['email'].apply(lambda x: \
            hashlib.sha256(x.encode('utf-8')).hexdigest())


    return df.to_csv()
    

@app.route('/')
def form():
    return '''
    <!doctype html>
        <style>
            div { margin: 10px }
            form { margin-left: 10px }
        </style>
        <title>데이터 암호 변환기(hash)</title>
        <h1>CSV 파일 데이터 단방향 암호화</h1>
        <div>1. 파일 선택 후, 암호화 실행 버튼을 눌러주세요</div>
        <div>2. 정상적인 파일 형식인 경우 암호화된 csv 파일을 다운로드 받을 수 있습니다.</div>
        <div>주의: 업로드할 CSV 파일의 처음 3개의 칼럼은 name, mobile, email 이어야 합니다. </div>
        <div>기타: 첫 3개 칼럼 이후 추가 칼럼은 가지고 있어도 상관 없습니다. </div>
        <form method=post action="/hash" enctype=multipart/form-data>
        <p><input type=file name=data_file></p>
        <p><input type=submit value=암호화_실행></p>
        </form>
    <div style="font-weight:bold;color:red">업로드된 데이터는 절대 저장되지 않습니다.</div>
    '''


@app.route('/hash', methods=["POST"])
def hash_data():
    file = request.files['data_file']
    if not file:
        return "No file"

    file_contents = file.stream.read().decode("utf-8")
    print('!@!@ file contents', file_contents)
    print('type of file contents', type(file_contents))


    result = hash_csv(io.StringIO(file_contents))

    print('@@@ result:', result)
    print('type result', type(result))

    # response = make_response(result)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=hashed_students.csv"
    response.headers["Content=Type"] = "text/csv"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


