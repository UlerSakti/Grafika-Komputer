Laporan Teknis Tugas 2: Transformasi Geometri 2D Interaktif

1. Identitas Mahasiswa

Nama Lengkap: M Raditya Zauhair

NIM: 2555200029

Mata Kuliah: Grafika Komputer

Prodi: Informatika

2. Screenshot Aplikasi

(Lampirkan berkas screenshot.png di dalam berkas .zip)

Transformasi Translasi & Rotasi

Transformasi Penskalaan (Scaling)



Program mengeksekusi matriks perkalian 3x3 secara real-time.

3. Penjelasan Matematis & Kode Program

A. Konsep Koordinat Homogen (Homogeneous Coordinates)

Untuk menggabungkan transformasi translasi, rotasi, dan penskalaan ke dalam satu perkalian matriks tunggal, koordinat 2D $(x, y)$ direpresentasikan dalam bentuk koordinat homogen 3D:


$$V = \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

B. Matriks Transformasi 2D (3x3)

Matriks Penskalaan (Scaling Matrix):


$$S(s_x, s_y) = \begin{bmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

Matriks Rotasi (Rotation Matrix):


$$R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

Matriks Translasi (Translation Matrix):


$$T(t_x, t_y) = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix}$$

C. Komposisi Matriks & Perkalian Vektor (NumPy)

Urutan perkalian matriks sangat penting agar objek berotasi dan berskala pada origin lokalnya sebelum ditranslasikan ke posisi kanvas:


$$M_{composite} = T(t_x, t_y) \times R(\theta) \times S(s_x, s_y)$$

Pada kode Python (main.py), operasi ini dieksekusi dengan operator perkalian matriks NumPy (@):

M = T @ R @ S
transformed_vertices = (M @ ORIGINAL_VERTICES.T).T


4. Petunjuk Menjalankan Program

A. Prasyarat

Pastikan Python versi 3.8 atau lebih baru telah terinstal di sistem Anda.

B. Langkah Eksekusi via Terminal/Command Prompt

Ekstrak Berkas Zip:
Ekstrak Tugas2_Grafkom_NIM_NamaLengkap.zip dan masuk ke direktori tersebut.

Instalasi Dependensi:

pip install -r requirements.txt


Jalankan Program Utama:

python main.py


5. Pemetaan Kontrol Keyboard

Panah Atas / Bawah / Kiri / Kanan: Menranslasikan (menggeser) pesawat di layar.

Tombol A / D: Memutar (rotasi) haluan pesawat secara clockwise / counter-clockwise.

Tombol + / -: Memperbesar atau memperkecil (penskalaan) ukuran pesawat.

Tombol R: Mengembalikan (reset) posisi, sudut, dan skala pesawat ke kondisi awal.

Tombol ESC: Keluar dari aplikasi.