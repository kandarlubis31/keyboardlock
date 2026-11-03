# keyboardlock — Project Context

## Ringkasan

Laptop Keyboard Manager: utilitas Windows kecil untuk menonaktifkan atau mengaktifkan kembali keyboard
bawaan laptop. Berguna saat keyboard mekanik diletakkan langsung di atas keyboard laptop sehingga
tombol tidak tertekan tanpa sengaja.

## Cara kerja

Keyboard internal laptop dikendalikan driver PS/2 `i8042prt`. Alat ini mengubah mode start driver
tersebut, jadi tidak ada hook tingkat rendah atau driver tambahan:

| Langkah | Detail |
| :--- | :--- |
| Baca status | `HKLM\SYSTEM\CurrentControlSet\Services\i8042prt` → nilai `Start` (`4` = nonaktif) |
| Nonaktifkan | `sc config i8042prt start= disabled` |
| Aktifkan | `sc config i8042prt start= auto` |

Perubahan baru berlaku setelah **restart**, karena driver dibaca saat boot. Aplikasi menampilkan
status saat ini supaya pengguna tahu apakah keyboard sedang dimatikan atau tidak.

Antarmuka memakai Python dengan `tkinter`, dibungkus jadi satu `.exe` (`keyboard_blocker_pro.py`
adalah berkas utamanya).

## Struktur

```
keyboard_blocker_pro.py   Aplikasi: deteksi status, tombol aktif/nonaktif, konfirmasi restart
requirements.txt          Dependensi Python
lock.ico                  Ikon aplikasi
```

## Menjalankan

```bash
pip install -r requirements.txt
python keyboard_blocker_pro.py
```

## Catatan penting

- **Wajib dijalankan sebagai Administrator** — mengubah layanan sistem ditolak tanpa hak itu.
- Jangan nonaktifkan keyboard sebelum keyboard eksternal terpasang dan berfungsi; kalau tidak, tidak
  ada input untuk menyalakannya kembali. Pemulihan lewat Safe Mode atau keyboard layar.
- Hanya menyentuh `i8042prt`, tidak menyentuh driver HID/USB, jadi keyboard eksternal tidak terpengaruh.
