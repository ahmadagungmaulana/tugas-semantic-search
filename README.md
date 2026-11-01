# Project: Semantic Search & Vector Database

## Informasi Project
- **Tema Dataset**: Game characters (Genshin Impact).
- **Fokus Data**: Karakter dari region Sumeru dan Fontaine (26 Karakter).
- **Tech Stack yang Digunakan**: FastAPI, Qdrant (In-Memory), dan Sentence-Transformers (all-MiniLM-L6-v2).

Aplikasi ini bisa mencari karakter Genshin Impact berdasarkan makna kata (lore/cerita) menggunakan teknologi AI, bukan sekadar mencari kecocokan kata persis.

---

### Experiment 1 - Semantic Search

#### Query 1
- **Query**: `"Dendro archon or ruler of Sumeru"`
- **Top Result**: Nahida
- **Similarity Score**: `  0.4049`
- **Hasil/Kecocokan**: hasilnya lumayan meski di angka yang tidak terlalu besar.

#### Query 2
- **Query**: `"Chief justice or hydro dragon sovereign of Fontaine"`
- **Top Result**: Neuvillette
- **Similarity Score**: `  0.4914`
- **Hasil/Kecocokan**: hasinya lumayan bagus angka hampir mendekati 0.50.

#### Query 3
- **Query**: `"Character raised in House of the Hearth"`
- **Top Result**: Freminet
- **Similarity Score**: `0.4236`
- **Hasil/Kecocokan**: bagus hasilnya sesuai/medekati karakter yang lahir di House of the Hearth.

#### Query 4
- **Query**: `"Sumeru scholar from Haravatat darshan"`
- **Top Result**: Alhaitham
- **Similarity Score**: ` 0.5231`
- **Hasil/Kecocokan**: Hasil yang bagus sesuai bahwa Alhaitam berasal dari sekolah Haravatat darshan.

#### Query 5
- **Query**: `"Warden or ruler of Fortress of Meropide"`
- **Top Result**: Sigewinne
- **Similarity Score**: ` 0.4204`
- **Hasil/Kecocokan**: Hasil nya lumayan meski menurut saya jawaban yang palisng sesuai harusnya Wriothesley.

---

### Experiment 2 - Top-K

- **Query**: `"Sumeru scholar from Haravatat darshan"`

**Top _k 1** 
- **character_name**: Alhaitham
- **Similarity Score**: ` 0.5231`

**Top _k 3**
- **character_name**: Alhaitham
- **Similarity Score**: ` 0.5231`
- **character_name**: Faruzan
- **Similarity Score**: ` 0.3557`
- **character_name**: Nahida
- **Similarity Score**: `  0.3505`

**Top _k 5**
- **character_name**: Alhaitham
- **Similarity Score**: ` 0.5231`
- **character_name**: Faruzan
- **Similarity Score**: ` 0.3557`
- **character_name**: Nahida
- **Similarity Score**: `  0.3505`
- **character_name**: Dehya
- **Similarity Score**: ` 0.3321`
- **character_name**: Kaveh
- **Similarity Score**: `  0.3196`

**Analisis**: Pada saat top_k di perbesar data mulai tidak sesuai seperti yang terjadi di top_k 3/5 ada Nahida dan Dehya dimana mereka bukan berasal dari Haravatat darshan, meski untuk Nahida masih masuk akal karena ada Kata akademiya pada affilation yang membuat score nya naik

---

### Experiment 3 - Bad Retrieval

- **Query**: `"Warden or ruler of Fortress of Meropide"`
- **Top_k 1**: Sigewinne
- **Similarity Score**: `   0.4204`

**Kenapa menurut kalian hasil tersebut kurang relevan?**
karena dalam game Sigewinne hanya seorang hanya kepala perawat di Meropide sedang kan kepala meropide adalah Wriothesley
dan yang aneh juga ketika top_k di perbesar nama Wriothesley tidak muncul.

**Menurut kalian apa yang mungkin menyebabkan hasil tersebut?**
kemungkinan penyebabnya adalah affiliation yang tidak spesifik dimana Sigewinne dan Wriothesley memiliki yang sama persis

---

## Personal Reflection
**1. Sebelum mengerjakan tugas ini, bagaimana kalian membayangkan sebuah search engine bekerja? Apakah ada perbedaan setelah mempelajari semantic search?**
sebelum mengerjakan banyangan saya sepeti yang telah saya pelajari yaitu dimana search engine bekerja dengan cara mencari score vektor terdekat atau paling mendekati 1, setelah mengerjakan tugas ini saya menjadi tau kalau search engine ini memiliki kekuranyan dimana semakin spesifik nya data maka akan akurat.

**2. Menurut kalian apa perbedaan terbesar antara keyword search dan semantic search?**
Perbedaannya terletak dari cara kerjanya. contoh keyword search, kalau kita mencari "Dendro archon" tapi di database hanya tertulis "Nahida" tanpa kata archon, pencariannya pasti gagal. Sedangkan pada semantic search, model akan menghubungkan makna kalau "Dendro archon" itu berkaitan erat dengan karakter "Nahida", sehingga sistem akan bisa menemukan hasil yang relevan/sesuai.

**3. Menurut kalian apa fungsi embedding di dalam semantic search?**
Embedding berfungsi sebagai penerjemah bahasa manusia ke bahasa mesin. dimana akan mengubah 1 kata utuh menjadi sebuah vektor atau angka yang mempresentasikan kata itu. angka/vektor ini nantinya akan digunakan untuk menghubungkan kata dengan kata lainya. 

**4. Kenapa embedding tidak cukup hanya disimpan di list Python jika jumlah data menjadi sangat banyak?**
selain repot kalu disimpan di list Python, penyebablainya karena akan memakan RAM yang sangan besar yang akan menyebabkan overhead.

**5. Bagian project mana yang paling sulit kalian pahami?**
Bagian yang cukup membingungkan bagi saya adalah setup Vector Database Qdrant terutama saat harus memahami perbedaan fungsi bawaan library-nya dan bagaimana membungkus format data asli JSON kita ke dalam atribut payload bersamaan dengan data vektornya.

**6. Bagian kode mana yang paling banyak dibantu oleh AI?**
Bagian awal ketika kode harus membaca file dataset.json, mengubah format teks menjadi vektor (encoding), dan melakukan proses iterasi untuk mengunggah (upsert) vektor tersebut ke dalam Qdrant Vector Database. lalu menangani perbaikan fungsi Qdrant yang sudah deprecated (ketinggalan versi).

**7. Jelaskan dengan bahasa kalian sendiri bagaimana bagian kode tersebut bekerja.**
penjelasan gampang nya ketika server baru mulai jalan, kode akan menyiapkan database kosong di Qdrant lalu membaca data dari dataset.json. dengan perulangan, data tiap karakter digabungin jadi satu kalimat utuh. kemudian Kalimat diubah jadi deretan angka (vektor) oleh model, agar mesin bisa mengerti maknanya. Terakhir, angka-angka itu disimpan ke database bersama data aslinya.

**8. Menurut kalian, aplikasi semantic search yang kalian buat bisa dikembangkan menjadi aplikasi apa jika project ini dilanjutkan?**
penggabungan dengan model lain(Gemini API) yang akan memperbagus (jadi lebih akurat) dalam menjelah carakter di game.

## AI Usage
**1. AI tools yang digunakan?**
Gemini AI.

**2. AI digunakan untuk membantu bagian apa?**
AI digunakan untuk debuging, menggunakan AI untuk memahami,membantu penulisan code yang benar (seperti cek,error,typo) dan membantu menyusun file README.md ini agar mudah dibaca.

**3. Bagian apa yang kalian ubah atau tentukan sendiri setelah mendapatkan hasil dari AI?**
bagian seperti menentukan kalau dataset terlalu besar, mengubah bagian AI yang merkomendasikan sesuatu yang belum pahami/pelajari, mengubah isi README.md dimana saya mengunakan AI hanya untuk membuat stuktur file yang mudah dibaca.
