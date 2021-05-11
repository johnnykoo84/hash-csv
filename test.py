import pandas as pd
import hashlib

# reading CSV input
df = pd.read_csv('student.csv')

# hashing the 'Password' column
df['name'] = df['name'].apply(lambda x: \
        hashlib.sha256(x.encode('utf-8')).hexdigest())

df['mobile'] = df['mobile'].apply(lambda x: \
        hashlib.sha256(x.encode('utf-8')).hexdigest())

df['email'] = df['email'].apply(lambda x: \
        hashlib.sha256(x.encode('utf-8')).hexdigest())

# writing the new CSV output
df.to_csv('student_hahsed.csv', index=False)