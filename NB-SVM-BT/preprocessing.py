import pandas as pd
import re

# ==========================================
# 0. LOAD DATA
# ==========================================
# Pastikan nama file ini sesuai dengan yang ada di folder komputermu
filename = 'bahlil_fix (1).xlsx'

try:
    df = pd.read_excel(filename)
except FileNotFoundError:
    print(f"Error: File '{filename}' tidak ditemukan.")
    exit()

# ==========================================
# 1. CLEANING
# ==========================================
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+', '', text)        # Hapus URL
    text = re.sub(r'@\w+', '', text)           # Hapus Mention
    text = re.sub(r'RT[\s]+', '', text)        # Hapus RT
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)   # Hapus non-huruf
    text = re.sub(r'\s+', ' ', text).strip()   # Hapus spasi berlebih
    return text

df['clean_text'] = df['full_text'].apply(clean_text)

print("--- 1. HASIL CLEANING (full_text vs clean_text) ---")
print(df[['full_text', 'clean_text']].head(5))
print("\n" + "-"*50 + "\n")

# ==========================================
# 2. CASE FOLDING
# ==========================================
df['case_folded_text'] = df['clean_text'].str.lower()

print("--- 2. HASIL CASE FOLDING (clean_text vs case_folded_text) ---")
print(df[['clean_text', 'case_folded_text']].head(5))
print("\n" + "-"*50 + "\n")

# ==========================================
# 3. NORMALISASI
# ==========================================
norm_dict = {
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
    'bbrp': 'beberapa', 'brp': 'berapa'
}

def normalize_text(text):
    words = text.split()
    normalized_words = [norm_dict.get(word, word) for word in words]
    return ' '.join(normalized_words)

df['normalized_text'] = df['case_folded_text'].apply(normalize_text)

print("--- 3. HASIL NORMALISASI (case_folded_text vs normalized_text) ---")
print(df[['case_folded_text', 'normalized_text']].head(5))
print("\n" + "-"*50 + "\n")

# ==========================================
# 4. TOKENISASI
# ==========================================
# Memecah kalimat menjadi list kata (tokens)
def tokenize_text(text):
    return text.split()

df['tokens'] = df['normalized_text'].apply(tokenize_text)

print("--- 4. HASIL TOKENISASI (normalized_text vs tokens) ---")
print(df[['normalized_text', 'tokens']].head(5))
print("\n")

# ==========================================
# SIMPAN KE EXCEL
# ==========================================
# Menyimpan hasil akhir (termasuk kolom tokens) ke file Excel baru
output_filename = 'hasil_preprocessing_tokenisasi.xlsx'

# Karena Excel tidak bisa menyimpan kolom tipe 'List' secara langsung dengan rapi,
# kita ubah tokens menjadi string dengan pemisah koma untuk penyimpanan (opsional),
# atau biarkan pandas menanganinya (akan tersimpan sebagai string representasi list).
# Di sini kita simpan apa adanya.
df.to_excel(output_filename, index=False)

print("="*50)
print(f"SUCCESS: Data berhasil disimpan ke file '{output_filename}'")
print("="*50)