# 🚀 APK Builder Tools - Konverter Web ke APK Modern

![Banner Proyek](https://raw.githubusercontent.com/bocil-termux/Buat_Sandi/refs/heads/main/file_000000005500622f977c3f8804e1b073.png)

## ⚠️ DISCLAIMER DAN PERINGATAN PENTING

**Pembuat alat ini (EyeFox) tidak bertanggung jawab atas penyalahgunaan tools ini untuk tujuan ilegal atau berbahaya.** 

- Tools ini dirancang untuk membantu developer web yang sah mengkonversi proyek mereka ke APK Android
- **Dilarang keras** menggunakan tools ini untuk:
  - Membuat aplikasi berisi malware
  - Melakukan aktivitas ilegal
  - Menyebarkan konten berbahaya
  - Melanggar hak cipta
- Pengguna bertanggung jawab penuh atas APK yang mereka buat
- Kami tidak menyimpan atau memantau proyek yang dibangun dengan tools ini

**Gunakanlah dengan bijak dan bertanggung jawab!**

## 📌 Gambaran Umum

Tools ini adalah alat canggih untuk mengkonversi proyek web (HTML/React) menjadi APK Android dengan berbagai opsi kustomisasi. Tool ini menyediakan:

- **Konversi Web ke APK** untuk proyek HTML dan React
- **Penandatanganan APK** dengan keystore kustom
- **Sistem Build Berbasis Cloud** untuk pembuatan APK efisien
- **Kustomisasi APK Profesional** termasuk:
  - Manajemen permission
  - Kontrol orientasi layar
  - Mode fullscreen
  - Kontrol versi
  - Kustomisasi ikon

## ✨ Fitur Utama

### 🔧 Fungsi Inti
- Konversi proyek HTML/React ke APK Android
- Hasilkan APK tertandatangani siap unggah ke Play Store
- Build berbasis cloud menghemat resource
- Sistem akses berbasis token

### 🛠️ Kustomisasi Lanjutan
- **Manajemen Izin**:
  - Pilih dari 14+ permission Android
  - Kontrol granular atas kemampuan aplikasi
- **Opsi Tampilan**:
  - Mode fullscreen (Immersive/Lean back)
  - Penguncian orientasi layar (Portrait/Landscape)
- **Konfigurasi Build**:
  - Manajemen versi kode/nama
  - Tipe build Debug/Release
  - ID aplikasi kustom

## 📦 Panduan Instalasi

```bash
pkg update && pkg upgrade -y
termux-setup-storage -y
pkg install python wget -y 
wget https://raw.githubusercontent.com/bocil-termux/build-apk/refs/heads/main/setup-build-apk.py > /dev/null 2>&1
pip install requests
python setup-build-apk.py
```

## 🛠️ Cara Penggunaan

### 1. Autentikasi
jalankan 
```bash
build-apk
```
Untuk menjalankan Tools

Pilih antara pendaftaran atau login untuk mengakses tools.

### 2. Menu Utama
- **Sign APK**: Tandatangani APK dengan keystore Anda
- **Buat Keystore**: Buat kunci penandatanganan baru
- **Build APK**: Konversi proyek web ke APK Android

### 3. Membangun APK
1. Proyek dan gambar harus berada pada direktori Acode
2. disarankan untuk menginstal aplikasi Acode di playstore untuk menulis coding
3. Pilih jenis proyek (HTML atau React)
4. Konfigurasi aplikasi:
   - Nama dan ID aplikasi
   - Informasi versi
   - Permission
   - Pengaturan tampilan
5. Tool akan:
   - Setup konfigurasi
   - Hasilkan file proyek Android
   - Build APK di cloud
   - Download APK yang sudah jadi

## 🌟 Contoh Alur Kerja

```mermaid
graph TD
    A[Mulai] --> B{Jenis Proyek?}
    B -->|HTML| C[Konfigurasi Proyek HTML]
    B -->|React| D[Konfigurasi Proyek React]
    C --> E[Atur Detail Aplikasi]
    D --> E
    E --> F[Pilih Permission]
    F --> G[Pilih Opsi Tampilan]
    G --> H[Konfigurasi Build]
    H --> I[Build di Cloud]
    I --> J[Download APK]
```

## 📊 Sistem Token

| Jenis Token  | Deskripsi                          | Cara Mendapatkan       |
|--------------|------------------------------------|------------------------|
| Token Aktif  | Dibutuhkan untuk build APK         | Beli dari admin        |
| Token Nonaktif| Bonus dari referral               | Referensikan pengguna baru |

## 🤝 Saran dan Kritik

Kami menerima semua saran yang diberikan untuk pengembangan tools ini. Harap gunakan tools ini hanya untuk tujuan yang baik dan legal.

## ✉️ Kontak

Kontak admin EyeFox yang bisa dihubungi:
- Nomor Wa: 087844072512
- Telegram: t.me/EyeFox123
- Grup Telegram: http://t.me/EyeFox_Group

## Salam hangat dari EyeFox 🦊

**Ingat:** Dengan menggunakan tools ini, Anda menyetujui bahwa Anda bertanggung jawab penuh atas APK yang dibuat dan akan menggunakan tools ini hanya untuk tujuan yang sah dan baik.
