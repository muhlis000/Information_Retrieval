import pandas as pd
import re
import sys

# Konfigurasi nama file
INPUT_FILENAME = 'bahlil_fix (1).xlsx'
OUTPUT_FILENAME = 'hasil_preprocessing_tokenisasi.xlsx'

# Kamus normalisasi
NORM_DICT = {
    'gak': 'tidak', 'ga': 'tidak', 'ngga': 'tidak', 'nggak': 'tidak',
    'gk': 'tidak', 'enggak': 'tidak', 'kagak': 'tidak',
    'udah': 'sudah', 'udh': 'sudah', 'dah': 'sudah',
    'bgt': 'banget', 'bener': 'benar',
    'emang': 'memang', 'emg': 'memang', 'emng': 'memang',
    'gimana': 'bagaimana', 'gmn': 'bagaimana', 'gmana': 'bagaimana',
    'knp': 'kenapa', 'knapa': 'kenapa',
    'sbg': 'sebagai', 'dgn': 'dengan', 'dg': 'dengan',
    'yg': 'yang', 'utk': 'untuk', 'krn': 'karena', 'krna': 'karena',
    'tp': 'tetapi', 'tapi': 'tetapi',
    'jd': 'jadi', 'jdi': 'jadi', 'jg': 'juga', 'jga': 'juga',
    'lg': 'lagi', 'lgi': 'lagi', 'sdg': 'sedang',
    'sy': 'saya', 'gw': 'saya', 'gue': 'saya', 'ane': 'saya',
    'lu': 'kamu', 'lo': 'kamu', 'elu': 'kamu',
    'org': 'orang', 'orng': 'orang',
    'mksh': 'terima kasih', 'tks': 'terima kasih', 'thx': 'terima kasih',
    'thanks': 'terima kasih', 'thank you': 'terima kasih',
    'ok': 'oke', 'oke': 'oke', 'okeh': 'oke',
    'mantap': 'bagus', 'mantul': 'bagus', 'keren': 'bagus',
    'jelek': 'buruk', 'payah': 'buruk', 'parah': 'buruk',
    'bgs': 'bagus', 'bgus': 'bagus',
    'hrs': 'harus', 'msti': 'harus', 'kudu': 'harus',
    'blm': 'belum', 'blom': 'belum',
    'skrg': 'sekarang', 'skr': 'sekarang', 'skrang': 'sekarang',
    'sm': 'sama', 'sama2': 'sama sama',
    'trs': 'terus', 'trus': 'terus',
    'sbnrnya': 'sebenarnya', 'sbnernya': 'sebenarnya',
    'bbrp': 'beberapa', 'brp': 'berapa', 'gitu': 'begitu', 
    'tak': 'tidak', 'klo': 'kalo', 'ni': 'ini', 
    'aja': 'saja', 'ngarep': 'berharap'
}

def clean_text(text):
    # Membersihkan teks dari URL, mention, RT, dan karakter non-alfabet
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+', '', text)        # Hapus URL
    text = re.sub(r'@\w+', '', text)           # Hapus Mention
    text = re.sub(r'RT[\s]+', '', text)        # Hapus RT
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)   # Hapus non-huruf
    text = re.sub(r'\s+', ' ', text).strip()   # Hapus spasi berlebih
    return text

def normalize_text(text):
    # Mengubah kata singkatan menjadi kata baku berdasarkan NORM_DICT
    words = text.split()
    normalized_words = [NORM_DICT.get(word, word) for word in words]
    return ' '.join(normalized_words)

def tokenize_text(text):
    # Memecah kalimat menjadi list kata (tokens)
    return text.split()

# 0. Load Data
try:
    df = pd.read_excel(INPUT_FILENAME)
except FileNotFoundError:
    print(f"Error: File '{INPUT_FILENAME}' tidak ditemukan.")
    sys.exit()

# 1. Cleaning
df['clean_text'] = df['full_text'].apply(clean_text)
print("Preview Cleaning:")
print(df[['full_text', 'clean_text']].head(5))

# 2. Case Folding
df['case_folded_text'] = df['clean_text'].str.lower()
print("\nPreview Case Folding:")
print(df[['clean_text', 'case_folded_text']].head(5))

# 3. Hapus Duplikat
jml_awal = len(df)
# Cek duplikat berdasarkan kolom 'case_folded_text'
df.drop_duplicates(subset=['case_folded_text'], keep='first', inplace=True)
df.reset_index(drop=True, inplace=True)
jml_akhir = len(df)

print(f"\nInfo Duplikat: Data awal {jml_awal}, Akhir {jml_akhir}, Dibuang {jml_awal - jml_akhir}")

# 4. Normalisasi
df['normalized_text'] = df['case_folded_text'].apply(normalize_text)
print("\nPreview Normalisasi:")
print(df[['case_folded_text', 'normalized_text']].head(5))

# 5. Tokenisasi
df['tokens'] = df['normalized_text'].apply(tokenize_text)
print("\nPreview Tokenisasi:")
print(df[['normalized_text', 'tokens']].head(5))

# Simpan ke Excel
df.to_excel(OUTPUT_FILENAME, index=False)
print(f"\nSUCCESS: Data berhasil disimpan ke file '{OUTPUT_FILENAME}'")