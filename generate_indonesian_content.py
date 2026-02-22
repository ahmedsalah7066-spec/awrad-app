import json
import os

# --- INDONESIAN TRANSLATIONS (Templated) ---

# --- DALAIL AL-KHAYRAT (Monolingual: Indonesian Content Only) ---
# Title MUST be translated.
# Content MUST be full Indonesian translation (no Arabic).
dalail_titles = {
    "saturday": "Hizb Hari Sabtu",
    "sunday": "Hizb Hari Ahad",
    "monday": "Hizb Hari Senin",
    "tuesday": "Hizb Hari Selasa",
    "wednesday": "Hizb Hari Rabu",
    "thursday": "Hizb Hari Kamis",
    "friday": "Hizb Hari Jumat"
}

dalail_translations = {
    "saturday": """Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang memegang amanah dan menyampaikan risalah.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau bukakan bagi kami pintu-pintu kebaikan, dan Engkau mudahkan bagi kami segala kesulitan.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya serta para sahabatnya, shalawat yang menjadi sebab pengampunan dosa-dosa dan pengangkatan derajat.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau selamatkan kami dari segala ketakutan dan bahaya, dan Engkau penuhi segala hajat kami.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau lepaskan ikatan lidahku, dan Engkau hilangkan kesusahanku.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, shalawat yang tiada akhirnya di alam semesta.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, selama bintang-bintang bersinar dan tanaman merambat berdaun.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, shalawat yang tak terhitung dan tak terbatas.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang layak dengan kedudukannya di sisi-Mu, dan dengannya Engkau sampaikan kami pada puncak harapan kami kepada-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang menjadi hijab bagi kami dari azab-Mu, dan sebab untuk meraih pahala-Mu.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak butiran pasir dan kerikil, dan sebanyak apa yang telah ada dan apa yang telah berlalu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang meridhainya dan dengannya Engkau muliakan keturunannya, dan dengannya Engkau sampaikan permintaannya pada hari kiamat.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang tidak usang barunya, dan tidak terhitung jumlahnya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Nabi yang banyak kembali (bertobat), Cahaya yang dengannya pintu-pintu dibuka.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang dengannya Engkau jadikan kami termasuk orang-orang yang sukses dan beruntung.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau beratkan timbangan kebaikan kami, dan dengannya Engkau ampuni dosa-dosa dan kesalahan kami.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang mendekatkan kami ke hadiratnya, dan membahagiakan kami dengan melihatnya.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, isteri-isterinya, dan keturunannya, sebanyak nafas umatnya.
Ya Allah, dengan berkah shalawat kepadanya, jadikanlah kami dengan shalawat kepadanya termasuk orang-orang yang beruntung, dan pada telaganya termasuk orang-orang yang datang dan minum, dan dengan sunnahnya dan ketaatannya termasuk orang-orang yang mengamalkan, dan janganlah Engkau halangi antara kami dan dia pada hari kiamat, wahai Tuhan semesta alam.

Dan ampunilah kami, orang tua kami, dan seluruh kaum Muslimin, dan segala puji bagi Allah Tuhan semesta alam.""",

    "sunday": """Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, shalawat yang menjadi cahaya bagi kami di atas Shirath, dan keselamatan dari azab.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau hilangkan kesedihan kami, dan Engkau lapangkan kegundahan dan kesusahan kami.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya kami dikaruniai kesempurnaan dalam mengikutinya, dan mengamalkan sunnahnya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang memenuhi ufuk dengan cahaya, dan menjadikan kami di dunia dan akhirat dalam kegembiraan dan kebahagiaan.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak apa yang ada di langit dan apa yang ada di bumi dan apa yang ada di antara keduanya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang menjadi penunaian bagi-Mu, dan pelaksanaan bagi haknya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang dengannya Engkau selamatkan pengucapnya dari api neraka Jahim.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang dengannya Engkau masukkan orang yang bershalawat ke dalam Surga Na'im.""",

    "monday": """Ya Allah, limpahkanlah shalawat kepada orang yang dengannya Engkau tutup kenabian dan risalah, Junjungan kami Muhammad.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Nabi yang Ummi, dan kepada keluarganya serta para sahabatnya, dan berilah salam.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang menjadi keridhaan bagi-Mu dan penunaian bagi haknya.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang memenuhi perbendaharaan Allah dengan cahaya, dan menjadi kelapangan dan kegembiraan bagi kami.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, pemilik Wasilah, Fadilah, dan Derajat yang Tinggi.
Ya Allah, sesungguhnya aku memohon kepada-Mu dengan permintaan-Mu yang terbaik, dan dengan nama-nama-Mu yang paling Engkau cintai, dan yang paling mulia di sisi-Mu, dan dengan apa yang Engkau anugerahkan kepada kami melalui Junjungan kami Muhammad Nabi kami shallallahu 'alaihi wa sallam, lalu Engkau selamatkan kami dengannya dari kesesatan, dan Engkau perintahkan kami untuk bershalawat kepadanya, dan Engkau jadikan shalawat kami kepadanya sebagai derajat, penebus dosa, kelembutan, dan anugerah dari pemberian-Mu; maka aku berdoa kepada-Mu sebagai pengagungan terhadap perintah-Mu, mengikuti wasiat-Mu, dan memohon syafaat Nabi-Mu Junjungan kami Muhammad shallallahu 'alaihi wa sallam.

Ya Allah, jadikanlah shalawat kami kepadanya diterima, dan doa kami dengannya dikabulkan, dan jadikanlah kami termasuk orang-orang yang mendapat syafaatnya.
Ya Allah, wahai Tuhan Muhammad dan keluarga Muhammad, limpahkanlah shalawat kepada Muhammad dan kepada keluarga Muhammad, dan balaslah Muhammad shallallahu 'alaihi wa sallam dengan apa yang pantas baginya.
Ya Allah, Tuhan segala roh dan jasad yang telah hancur, aku memohon kepada-Mu dengan kepatuhan roh-roh yang kembali kepada jasadnya, dan dengan kepatuhan jasad-jasad yang menyatu kembali dengan urat-uratnya, dan dengan kalimat-kalimat-Mu yang berlaku pada mereka, dan pengambilan-Mu akan kebenaran dari mereka, sedangkan makhluk-makhluk berada di hadapan-Mu menunggu keputusan hukum-Mu, mengharapkan rahmat-Mu, dan takut akan hukuman-Mu, agar Engkau menjadikan cahaya pada penglihatanku, dan zikir kepada-Mu siang dan malam di lidahku, dan rezekikanlah aku amal saleh.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad selama gunung-gunung berjalan, sungai-sungai mengalir, matahari bersinar, dan siang menerangi.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad sebagaimana yang Engkau cintai dan ridhai baginya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang dengannya Engkau selamatkan kami dari segala huru-hara dan bencana, dan Engkau penuhi segala hajat kami, dan Engkau sucikan kami dengannya dari segala keburukan, dan Engkau angkat kami dengannya di sisi-Mu ke derajat yang paling tinggi, dan Engkau sampaikan kami dengannya pada tujuan yang paling jauh dari segala kebaikan dalam kehidupan dan setelah mati.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat keridhaan, dan ridhailah para sahabatnya dengan keridhaan yang sempurna.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang cahayanya mendahului penciptaan, dan kemunculannya adalah rahmat bagi semesta alam, sebanyak makhluk-Mu yang telah lalu dan yang masih ada, dan siapa yang bahagia di antara mereka dan siapa yang celaka, shalawat yang melampaui hitungan dan meliputi batasan, shalawat yang tidak ada tujuannya, tidak ada akhirnya, dan tidak ada habisnya, shalawat yang kekal dengan kekekalan-Mu, dan kepada keluarganya serta para sahabatnya, dan berilah salam dengan salam yang seperti itu.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad yang telah Engkau penuhi hatinya dengan keagungan-Mu, dan matanya dengan keindahan-Mu, sehingga dia menjadi bahagia dan gembira, didukung dan ditolong, dan kepada keluarganya serta para sahabatnya, dan berilah salam yang banyak, dan segala puji bagi Allah atas hal itu.""",


    "tuesday": """Ya Allah, sesungguhnya aku memohon kepada-Mu dari kebaikan apa yang Engkau ketahui, dan aku berlindung kepada-Mu dari keburukan apa yang Engkau ketahui, dan aku memohon ampunan-Mu dari segala apa yang Engkau ketahui, sesungguhnya Engkau Maha Mengetahui hal-hal yang ghaib.
Ya Allah, rahmatilah aku dari zamanku ini dan penduduknya, dan gabungkanlah aku dengan hamba-hamba-Mu yang saleh.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang menjadi keridhaan bagi-Mu, dan penunaian bagi haknya, dan berikanlah kepadanya Wasilah dan Maqam Mahmud yang telah Engkau janjikan, dan balaslah dia dari kami dengan apa yang pantas baginya, dan balaslah dia dengan balasan yang lebih utama dari apa yang Engkau balaskan kepada seorang Nabi dari kaumnya dan seorang Rasul dari umatnya, dan limpahkanlah shalawat kepada seluruh saudaranya dari para Nabi dan Orang-Orang Saleh, wahai Yang Paling Penyayang di antara para penyayang.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan tempatkanlah dia pada kedudukan yang dekat di sisi-Mu pada hari kiamat.
Ya Allah, jadikanlah shalawat-Mu, rahmat-Mu, dan berkah-Mu kepada Penghulu para Rasul, Imam orang-orang bertakwa, dan Penutup para Nabi, Junjungan kami Muhammad hamba-Mu dan Rasul-Mu, Imam Kebaikan, Pemimpin Kebaikan, dan Rasul Rahmat.
Ya Allah, bangkitkanlah dia pada Maqam Mahmud yang diinginkan oleh orang-orang terdahulu dan orang-orang kemudian.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad sebagaimana Engkau telah bershalawat kepada Junjungan kami Ibrahim dan kepada keluarga Junjungan kami Ibrahim, sesungguhnya Engkau Maha Terpuji lagi Maha Mulia. Ya Allah, berkahilah Junjungan kami Muhammad dan keluarga Junjungan kami Muhammad sebagaimana Engkau telah memberkahi Junjungan kami Ibrahim dan keluarga Junjungan kami Ibrahim, sesungguhnya Engkau Maha Terpuji lagi Maha Mulia.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad hamba-Mu dan Rasul-Mu, dan limpahkanlah shalawat kepada orang-orang mukmin laki-laki dan perempuan, serta orang-orang muslim laki-laki dan perempuan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarganya sebanyak apa yang diliputi oleh ilmu-Mu, dan dihitung oleh kitab-Mu, dan disaksikan oleh malaikat-Mu, shalawat yang kekal abadi dengan kekekalan kerajaan Allah.

Ya Allah, sesungguhnya aku memohon kepada-Mu dengan seluruh Asmaul Husna-Mu, agar Engkau melimpahkan shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad dengan setiap shalawat yang pernah diucapkan kepadanya dari awal masa hingga akhirnya, dan agar Engkau menjadikan shalawat kami ini seperti shalawat mereka, dan pahala kami seperti pahala mereka, dan agar Engkau melipatgandakan hal itu bagi kami dengan karunia-Mu, wahai Yang Paling Mulia di antara para mulia.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Nabi yang Zuhud, Rasul Raja Yang Maha Esa lagi Tempat Bergantung Segala Sesuatu, semoga Allah melimpahkan shalawat dan salam kepadanya, shalawat yang kekal hingga akhir masa, tanpa terputus dan tanpa habis, shalawat yang dengannya Engkau selamatkan kami dari panasnya neraka Jahanam dan seburuk-buruk tempat tinggal.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang belum pernah diucapkan oleh orang yang bershalawat sejak awal masa, dan shalawat yang akan diucapkan oleh orang-orang yang bershalawat hingga akhir masa, seperti keutamaan shalawat mereka atas shalawatnya, dan seperti keutamaan dia atas seluruh makhluk-Nya, dan limpahkanlah shalawat kepadanya dan kepada keluarganya, shalawat yang layak dengan kemuliaan dan kedudukannya yang agung.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Lautan yang Penuh, dan Cahaya yang Bersinar, shalawat yang memenuhi segala penjuru, dan menjadi keselamatan bagi kami dari Neraka.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarganya serta para sahabatnya, shalawat yang tidak ada akhir bagi kesempurnaannya, dan tidak ada kebinasaan bagi kekekalannya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang menjadi pendekatan diri kepada-Mu, dan balasan baginya, dan kebaikan bagi kami.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad yang merupakan Kutub Keagungan, Matahari Kenabian dan Risalah, Penunjuk kepada-Mu, dan Pembimbing kepada-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarganya, dan rasakanlah kepada kami manisnya perjumpaan dengannya, dan jadikanlah kami termasuk ahli kesempurnaannya, dan segala puji bagi Allah atas hal itu.""",

    "wednesday": """Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang kekal dengan kekekalan-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang tiada habisnya sebagaimana tiada akhir bagi kesempurnaan-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarganya, shalawat yang layak dengan keindahan, keagungan, dan kesempurnaannya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarganya, dan rasakanlah kepada kami dengan shalawat kepadanya lezatnya perjumpaan dengannya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Nabi-Mu yang Terpilih, Rasul-Mu yang Diridhai, Kekasih-Mu yang Dipilih, dan Kepercayaan-Mu atas wahyu langit.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Leluhur yang Paling Mulia, yang Dimuliakan di segala penjuru, yang Disifati dengan sifat-sifat yang mulia.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang cahayanya mendahului seluruh makhluk, dan kemunculannya adalah rahmat bagi semesta alam.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, pemilik Telaga yang Didatangi, Maqam yang Terpuji, dan Panji yang Terikat.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang merupakan sebaik-baik orang yang berdiri dan duduk, dan semulia-mulia orang yang menyaksikan dan disaksikan.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang menambah kebaikan kami, dan dengannya Engkau hapuskan keburukan kami, dan dengannya Engkau tinggikan derajat kami.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang tidak dapat dikejar oleh siapa pun, dan tidak dapat diungguli oleh siapa pun.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang menjadi cahaya dan petunjuk bagi kami, serta sandaran dan pertolongan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak apa yang ada dalam ilmu Allah, shalawat yang kekal dengan kekekalan kerajaan Allah.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang mewajibkan syafaatnya bagi kami, mendekatkan kami ke hadiratnya, dan membawa kami ke telaganya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau sampaikan kami di dua negeri pada Wasilah-nya yang agung.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang menyifati-Mu, yang menunjukkan kepada-Mu, yang menegakkan hak-Mu, dan yang menjelaskan perintah-Mu.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau hilangkan kesusahan, Engkau perbaiki hati, dan Engkau ampuni dosa-dosa.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang datang dengan Kebenaran yang nyata, dan diutus sebagai rahmat bagi semesta alam.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebagaimana Engkau perintahkan kami untuk bershalawat kepadanya, dan limpahkanlah shalawat kepadanya sebagaimana seharusnya shalawat diucapkan kepadanya.

Ya Allah, limpahkanlah shalawat kepada Nabi-Mu yang Terpilih, Rasul-Mu yang Diridhai, Kekasih-Mu yang Dipilih, dan kepada keluarganya, sahabatnya, isteri-isterinya, dan keturunannya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarganya, shalawat yang meridhakan-Mu dan meridhakan-nya, dan dengannya Engkau ridha kepada kami wahai Yang Paling Penyayang di antara para penyayang.
Ya Allah, Tuhan Baitul Haram, dan Tuhan Rukun dan Maqam, sampaikanlah salam dari kami kepada Junjungan kami, Tuan kami, dan Pemberi Syafaat kami, Muhammad.""",

    "thursday": """Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, makhluk yang paling mulia, dan penghulu penduduk bumi dan langit.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang layak dengan zatnya yang mulia, dan menjadi penjagaan bagi kami dari pelanggaran.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya serta para sahabatnya, shalawat yang kekal hingga hari pembalasan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, selama matahari terbit, dan selama shalat lima waktu didirikan, dan selama pembicara berbicara dengan bisikan.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang Engkau pantas untuknya, dan dia pantas untuknya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, sebagaimana dia pantas dan berhak mendapatkannya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan balaslah dia dari kami dengan sebaik-baik balasan yang Engkau berikan kepada seorang Nabi dari umatnya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, sejumlah setiap zarrah sejuta kali.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang menimbang bumi dan langit.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, sepenuh apa yang Engkau ciptakan, dan seberat Arsy-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, shalawat yang tidak ada putusnya dan tidak ada hilangnya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang menjadi simpanan dan pemberian bagi kami.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak daun pepohonan, ombak lautan, dan tetesan air hujan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau angkat derajat kami, Engkau mudahkan urusan kami, dan Engkau terangi cahaya kami.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau lapangkan dada kami, dan Engkau berkahi urusan kami.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau muliakan tempat tinggalnya, dan Engkau sampaikan keridhaannya pada hari kiamat.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Nabi yang Sejati, Tuan yang Mulia, yang datang dengan Wahyu dan Penurunan, dan menjelaskan keterangan takwil.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, sahabat-sahabatnya, isteri-isterinya, keturunannya, dan ahli baitnya, dengan shalawat yang paling utama, salam yang paling suci, dan berkah yang paling berkembang, di setiap waktu dan saat.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, selama orang-orang yang berzikir mengingatnya, dan orang-orang yang lalai melupakan mengingatnya.

Ya Allah, limpahkanlah shalawat kepada Nabi Rahmat, Pemberi Syafaat Umat, dan Penghilang Kesedihan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya kami memperoleh syafaatnya, dan mendapatkan kebahagiaan dengan menemaninya di Surga.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, dan ampunilah kami, orang tua kami, dan seluruh kaum Muslimin, dan segala puji bagi Allah Tuhan semesta alam.""",

    "friday": """Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad dan kepada keluarga Junjungan kami Muhammad, shalawat yang menjadi kelapangan bagi kami dari setiap kesedihan, dan jalan keluar dari setiap kesusahan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang meridhakan-Mu dan meridhakan-nya, dan dengannya Engkau ridha kepada kami, wahai Tuhan semesta alam.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Cahaya dari segala Cahaya, Rahasia dari segala Rahasia, dan Penghulu orang-orang yang berbakti.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang terpilih untuk Kepemimpinan dan Risalah sebelum penciptaan malam dan siang.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, di kalangan orang-orang terdahulu, dan limpahkanlah shalawat kepada Junjungan kami Muhammad di kalangan orang-orang kemudian, dan limpahkanlah shalawat kepada Junjungan kami Muhammad di kalangan para Nabi, dan limpahkanlah shalawat kepada Junjungan kami Muhammad di kalangan para Rasul, dan limpahkanlah shalawat kepada Junjungan kami Muhammad di kalangan Malaikat Tertinggi hingga hari pembalasan.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang tidak terhitung dan tidak terbatas, tidak ada caranya dan tidak ada masanya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang merupakan Roh Kehidupan, dan Pintu Keselamatan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebaik-baik Nabi-Mu, semulia-mulia Pilihan-Mu, Imam Para Wali-Mu, dan Penutup Para Nabi-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada Ahli Baitnya yang baik lagi suci, dan kepada para sahabatnya yang mulia lagi diberkahi.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang bersambung, berulang hingga hari pembalasan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, Nabi yang Ummi, yang Suci lagi Bersih, shalawat yang dengannya ikatan-ikatan terlepas, da kesusahan-kesusahan terurai.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, sebanyak apa yang Engkau ciptakan, sebanyak apa yang Engkau rezekikan, sebanyak apa yang Engkau hidupkan, dan sebanyak apa yang Engkau matikan.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau jadikan bagi kami jalan keluar dari setiap kesempitan, dan kelapangan dari setiap kesedihan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang dengan cahayanya kegelapan menjadi terang.
Ya Allah, limpahkanlah shalawat kepada Nabi yang diutus sebagai rahmat bagi seluruh umat.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, shalawat yang memenuhi tiang-tiang Arsy-Mu, dan sebanyak tinta kalimat-kalimat-Mu.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang dengannya Engkau bukakan bagi kami pintu-pintu keridhaan dan kemudahan, dan dengannya Engkau tutup bagi kami pintu-pintu keburukan dan kesulitan.
Ya Allah, limpahkanlah shalawat kepada orang yang dengannya Engkau bersumpah dalam Kitab-Mu yang nyata, lalu Engkau berfirman dan firman-Mu adalah Benar: {Demi umurmu, sesungguhnya mereka benar-benar dalam kemabukan mereka terombang-ambing}.
Ya Allah, limpahkanlah shalawat kepada orang yang Engkau ajak bicara dengan firman-Mu: {Dan sesungguhnya engkau benar-benar berbudi pekerti yang agung}.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak kebaikan Junjungan kami Adam 'alaihis salam.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak apa yang Junjungan kami Nuh 'alaihis salam berdoa kepada-Mu dengannya.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak apa yang Junjungan kami Yunus 'alaihis salam bertasbih kepada-Mu dengannya di dalam perut ikan.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak apa yang Kekasih-Mu Junjungan kami Ibrahim 'alaihis salam berkata kepada-Nya: {Perlihatkanlah kepadaku bagaimana Engkau menghidupkan orang-orang mati}.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sejumlah setiap huruf yang ditulis oleh Qalam di Ummul Kitab.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang kekal dengan kekekalan-Mu, abadi dengan keabadian-Mu, tidak ada akhirnya tanpa ilmu-Mu.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, shalawat yang meridhakan-Mu dan meridhakan-nya, dan dengannya Engkau ridha kepada kami wahai Tuhan semesta alam.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sebanyak apa yang telah terjadi, dan sebanyak apa yang akan terjadi, dan sebanyak apa yang ada dalam ilmu Allah yang tersembunyi.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, yang di langit adalah Mahmud (Terpuji), dan di bumi adalah Muhammad (Terpuji).
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, sehingga tidak tersisa sedikit pun dari shalawat.
Dan berkahilah Junjungan kami Muhammad, sehingga tidak tersisa sedikit pun dari keberkahan.
Dan rahmatilah Junjungan kami Muhammad, sehingga tidak tersisa sedikit pun dari rahmat.
Dan berilah salam kepada Junjungan kami Muhammad, sehingga tidak tersisa sedikit pun dari salam.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, di dalam roh-roh, dan kepada jasadnya di dalam jasad-jasad, dan kepada kuburnya di dalam kubur-kubur.
Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, hamba-Mu, Nabi-Mu, dan Rasul-Mu, Nabi yang Ummi, dan kepada keluarga Junjungan kami Muhammad.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarga Junjungan kami Muhammad, sebanyak apa yang diliputi oleh ilmu-Mu, dan ditulis oleh pena-Mu, dan didahului oleh kehendak-Mu, dan didoakan oleh malaikat-Mu, shalawat yang kekal dengan kekekalan-Mu, abadi dengan karunia dan kebaikan-Mu, hingga abadi selamanya, yang tidak ada akhir bagi keabadiannya, dan tidak ada kebinasaan bagi kekekalannya.

Ya Allah, limpahkanlah shalawat kepada Junjungan kami Muhammad, dan kepada keluarganya, dan ridhailah para sahabatnya, dan ampunilah orang-orang mukmin laki-laki dan perempuan, dan orang-orang muslim laki-laki dan perempuan, yang masih hidup di antara mereka dan yang sudah mati.

Ya Allah, Wahai Pemilik Karunia yang Agung, dan Wahai Pemilik Pemberian yang Besar, dan Wahai Pemilik Kedermawanan dan Kemuliaan, kami memohon kepada-Mu agar Engkau melimpahkan shalawat kepada Junjungan kami Muhammad, dan agar Engkau membalasnya dari kami dengan sebaik-baik balasan, dan agar Engkau menerima dari kami apa yang telah kami baca, dan menjadikannya cahaya yang berjalan di hadapan kami, dan pemberi syafaat bagi kami pada hari kiamat.

Ya Allah, akhirilah hidup kami dengan amal-amal saleh, dan wafatkanlah kami dalam keimanan yang sempurna, dan jadikanlah akhir ucapan kami di dunia "La ilaha illallah, Muhammadur Rasulullah".
Dan segala puji bagi Allah Tuhan semesta alam."""
}

# --- MUNAJAT (Monolingual: Indonesian Content Only) ---
munajat_titles_id = {
    "munajat_taibin": "Munajat Orang-Orang yang Bertobat",
    "munajat_shakin": "Munajat Orang-Orang yang Mengadu",
    "munajat_khaifin": "Munajat Orang-Orang yang Takut",
    "munajat_rajin": "Munajat Orang-Orang yang Berharap",
    "munajat_raghibin_2": "Munajat Para Pencinta",
    "munajat_shakirin": "Munajat Orang-Orang yang Bersyukur",
    "munajat_mutiin": "Munajat Orang-Orang yang Taat",
    "munajat_muridin": "Munajat Para Murid",
    "munajat_muhibbin": "Munajat Para Pecinta",
    "munajat_raghibin_1": "Munajat Orang-Orang yang Bertawassul",
    "munajat_muftaqirin": "Munajat Orang-Orang yang Fakir",
    "munajat_arifin": "Munajat Orang-Orang yang Arif",
    "munajat_dhakirin": "Munajat Orang-Orang yang Berdzikir",
    "munajat_mutawassilin": "Munajat Orang-Orang yang Memohon Perlindungan",
    "munajat_zahidin": "Munajat Orang-Orang yang Zuhud"
}

munajat_translations = {
    "munajat_taibin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, dosa-dosa telah memakaikanku pakaian kehinaan, dan kejauhan dari-Mu telah menyelimutiku dengan pakaian kemiskinan, dan besarnya kejahatanku telah mematikan hatiku. Maka hidupkanlah ia dengan tobat kepada-Mu, wahai Harapanku dan Tujuan-ku, wahai Permintaanku dan Cita-citaku. Demi Kemuliaan-Mu, aku tidak menemukan pengampun bagi dosa-dosaku selain Engkau, dan aku tidak melihat penambal bagi kerusakanku selain Engkau. Aku telah tunduk dengan kembali kepada-Mu, dan aku merendahkan diri dengan ketundukan di hadapan-Mu. Jika Engkau mengusirku dari pintu-Mu, maka kepada siapa aku berlindung? Dan jika Engkau menolakku dari sisi-Mu, maka kepada siapa aku bernaung? Duhai penyesalanku atas rasa maluku dan aibku! Duhai kesedihanku atas buruknya amalku dan kejahatanku!

Aku memohon kepada-Mu, wahai Pengampun dosa besar, wahai Penambal tulang yang patah, agar Engkau mengampuni dosa-dosaku yang membinasakan, dan menutupi aib-aibku yang memalukan, dan janganlah Engkau hinakan aku pada hari ketika rahasia-rahasia diuji, dan aib serta keburukan ditampakkan, hari di mana "harta dan anak-anak tidak berguna, kecuali orang yang datang kepada Allah dengan hati yang selamat."

Wahai Tuhanku, sesungguhnya aku menghadap kepada-Mu dengan Muhammad Nabi-Mu, Nabi pembawa rahmat, semoga Allah melimpahkan shalawat kepadanya dan keluarganya, agar Engkau mengampuni ketergelinciranku, menghilangkan kesusahanku, dan memenuhi hajatku.

Wahai Tuhanku, Engkaulah yang membuka pintu ampunan-Mu bagi hamba-hamba-Mu yang Engkau namakan Tobat. Engkau berfirman: "Bertobatlah kepada Allah dengan tobat yang semurni-murninya." Maka apa alasan bagi orang yang lalai memasuki pintu itu setelah dibukakan?

Wahai Tuhanku, jika dosa dari hamba-Mu itu buruk, maka biarlah maaf dari sisi-Mu itu indah.

Wahai Tuhanku, aku bukanlah orang pertama yang mendurhakai-Mu lalu Engkau terima tobatnya, dan menghadapkan diri pada kebaikan-Mu lalu Engkau bermurah hati kepadanya. Wahai Pengabul doa orang yang dalam kesulitan, wahai Penghilang bahaya, wahai Yang Maha Besar kebaikan-Nya, wahai Yang Maha Mengetahui apa yang tersembunyi, wahai Yang Indah tirai penutup-Nya; aku memohon syafaat dengan kedermawanan dan kemuliaan-Mu kepada-Mu, dan aku bertawassul dengan kasih sayang dan rahmat-Mu di sisi-Mu. Maka kabulkanlah doaku, janganlah Engkau kecewakan harapanku kepada-Mu, terimalah tobatku, dan hapuskanlah kesalahanku, dengan karunia dan rahmat-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_shakin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, kepada-Mu aku mengadukan nafsu yang selalu menyuruh kepada keburukan, bersegera menuju dosa, sangat gemar akan maksiat kepada-Mu, dan menjerumuskan pada kemurkaan-Mu. Ia membawaku menempuh jalan-jalan kebinasaan, dan menjadikanku orang binasa yang paling hina di sisi-Mu. Banyak penyakitnya, panjang angan-angannya. Jika ditimpa keburukan ia berkeluh kesah, dan jika mendapat kebaikan ia kikir. Cenderung kepada permainan dan kelalaian, penuh dengan kelengahan dan kelupaan. Ia mempercepatku menuju dosa, dan menunda-nundaku untuk bertobat.

Wahai Tuhanku, aku mengadu kepada-Mu tentang musuh yang menyesatkanku, dan setan yang menggelincirkanku. Ia telah memenuhi dadaku dengan waswas, dan bisikan-bisikannya telah mengepung hatiku. Ia membantuku untuk mengikuti hawa nafsu, menghiasi cinta dunia bagiku, dan menghalangi antara aku dan ketaatan serta kedekatan kepada-Mu.

Wahai Tuhanku, kepada-Mu aku mengadukan hati yang keras, yang berbolak-balik bersama waswas, yang diselimuti oleh noda dan cap kelalaian; dan mata yang beku dari menangis karena takut kepada-Mu, namun berambisi memandang apa yang menyenangkannya.

Wahai Tuhanku, tiada daya dan upaya bagiku kecuali dengan kekuatan-Mu, dan tiada keselamatan bagiku dari hal-hal yang tidak disukai di dunia kecuali dengan penjagaan-Mu. Maka aku memohon kepada-Mu dengan kebalighan hikmah-Mu dan terlaksananya kehendak-Mu, agar Engkau tidak menjadikanku sasaran bagi selain kedermawanan-Mu, dan tidak menjadikanku target bagi fitnah-fitnah. Jadilah Penolong bagiku atas musuh-musuh, Penutup bagi aib dan cacat, Pelindung dari bencana, dan Penjaga dari kemaksiatan, dengan kasih sayang dan rahmat-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_khaifin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, apakah Engkau akan menyiksaku setelah aku beriman kepada-Mu? Atau menjauhkanku setelah aku mencintai-Mu? Atau menghalangiku padahal aku mengharapkan rahmat dan ampunan-Mu? Atau menyerahkanku (kepada azab) padahal aku berlindung dengan maaf-Mu? Jauh dari Wajah-Mu yang Mulia untuk mengecewakanku! Duhai kiranya, apakah ibuku melahirkanku untuk kesengsaraan? Atau membesarkanku untuk penderitaan? Duhai seandainya dia tidak melahirkanku dan tidak membesarkanku! Dan duhai seandainya aku tahu, apakah Engkau menjadikanku termasuk ahli sa'adah (orang-orang yang berbahagia), dan mengkhususkanku dengan kedekatan dan tetangga-Mu? Sehingga mataku menjadi sejuk karenanya dan jiwaku menjadi tenang.

Wahai Tuhanku, apakah Engkau akan menghitamkan wajah-wajah yang tunduk bersujud karena keagungan-Mu? Atau membungkam lidah-lidah yang mengucapkan pujian atas kemuliaan dan kebesaran-Mu? Atau menutup hati-hati yang terlipat atas cinta kepada-Mu? Atau mentulikan telinga-telinga yang menikmati mendengarkan zikir-Mu? Atau membelenggu tangan-tangan yang diangkat oleh harapan kepada-Mu mengharap belas kasih-Mu? Atau menyiksa kaki-kaki yang berusaha dalam ibadah kepada-Mu?

Wahai Tuhanku, janganlah Engkau tutup pintu-pintu rahmat-Mu bagi orang-orang yang mentauhidkan-Mu, dan janganlah Engkau halangi orang-orang yang merindukan-Mu dari memandang keindahan Wajah-Mu.

Wahai Tuhanku, jiwa yang telah Engkau muliakan dengan tauhid-Mu, bagaimana mungkin Engkau hinakan dengan kehinaan hiran (pengabaian)-Mu? Dan hati yang telah terikat dengan cinta-Mu, bagaimana mungkin Engkau bakarnya dengan panas api-Mu?

Wahai Tuhanku, lindungilah aku dari pedihnya murka-Mu dan besarnya kemarahan-Mu. Wahai Yang Maha Lembut, wahai Yang Maha Pemberi, wahai Yang Maha Penyayang, wahai Yang Maha Pengasih, wahai Yang Maha Perkasa, wahai Yang Maha Memaksa, wahai Yang Maha Pengampun, wahai Yang Maha Menutup Aib. Selamatkanlah aku dengan rahmat-Mu dari azab neraka, dan skandal aib, ketika orang-orang baik dipisahkan dari orang-orang jahat, dan keadaan berubah menjadi mengerikan, dan orang-orang yang berbuat baik didekatkan, dan orang-orang yang berbuat jahat dijauhkan, dan setiap jiwa dibalas apa yang telah diusahakannya dan mereka tidak dirugikan.""",

    "munajat_rajin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, jika bekalku sedikit dalam perjalanan menuju-Mu, sungguh prasangkaku telah baik dalam bertawakal kepada-Mu. Jika kejahatanku telah membuatku takut akan hukuman-Mu, sesungguhnya harapanku telah membuatku merasa aman dari balasan-Mu. Jika dosaku telah menghadapkanku pada siksa-Mu, sungguh kepercayaanku yang baik akan pahala-Mu telah memberitahuku. Jika kelalaian telah menidurkanku dari bersiap untuk bertemu dengan-Mu, sungguh pengetahuan akan kedermawanan dan nikmat-Mu telah membangunkanku. Dan jika keterlaluan dalam maksiat dan kedurhakaan telah membuat apa yang ada antara aku dan Engkau menjadi sunyi, sungguh kabar gembira ampunan dan keridhaan telah menghiburku.

Aku memohon kepada-Mu dengan keagungan Wajah-Mu dan cahaya kesucian-Mu, dan aku memohon kepada-Mu dengan kelembutan rahmat-Mu dan halusnya kebaikan-Mu, agar Engkau mewujudkan prasangkaku dalam apa yang aku harapkan dari pahala-Mu yang besar, dan membenarkan harapanku dalam apa yang aku nantikan dari tempat kembali yang indah.

Wahai Tuhanku, apa yang akan Engkau perbuat terhadap orang yang menjadikan harapannya pada keindahan maaf-Mu, dan berusaha mencari keridhaan-Mu, dan menyerahkan tangannya pada tali ketaatan-Mu, dan bergantung pada sebab-sebab cinta-Mu, dan bersimpuh di pintu kedermawanan-Mu, dan menuju ke sisi rahmat-Mu, dan mengharapkan keutamaan pemberian-Mu, dan berlindung dengan keindahan tutupan-Mu, dan bernaung di bawah naungan maaf-Mu?

Wahai Tuhanku, janganlah Engkau kecewakan orang yang tidak menemukan pemberi selain Engkau, dan janganlah Engkau tolak orang yang tidak menemukan tempat berharap selain Engkau. Maka apa yang telah Engkau nikmatkan, janganlah Engkau cabut; dan apa yang telah Engkau anugerahkan kepadaku dari kemuliaan-Mu, janganlah Engkau ambil; dan apa yang telah Engkau tutupi atasku dengan kesantunan-Mu, janganlah Engkau singkap; dan apa yang Engkau ketahui dari buruknya perbuatanku, ampunilah.

Wahai Tuhanku, aku memohon syafaat dengan-Mu kepada-Mu, dan aku berlindung dengan-Mu dari-Mu. Aku datang kepada-Mu dengan mengharap kebaikan-Mu, menginginkan anugerah-Mu, memohon curahan kemurahan-Mu, mengharap hujan awan keutamaan-Mu, mencari keridhaan-Mu, menuju sisi-Mu, mendatangi syariat pemberian-Mu, memohon kebaikan-kebaikan yang luhur dari sisi-Mu, bertamu ke hadirat keindahan-Mu, menginginkan Wajah-Mu, mengetuk pintu-Mu, tunduk pada keagungan dan kebesaran-Mu. Maka perbuatlah padaku apa yang pantas bagi-Mu berupa ampunan dan rahmat, dan jangan perbuat padaku apa yang pantas bagiku berupa azab dan balasan, dengan rahmat-Mu wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_raghibin_2": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Dzat yang jika seorang hamba meminta kepada-Nya, Dia memberinya; dan jika dia berharap apa yang ada di sisi-Nya, Dia menyampaikannya pada cita-citanya; dan jika dia menghadap kepada-Nya, Dia mendekatkannya dan merapatinya; dan jika dia terang-terangan bermaksiat kepada-Nya, Dia menutupinya dan melindunginya; dan jika dia bertawakal kepada-Nya, Dia mencukupinya.

Wahai Tuhanku, siapakah yang singgah pada-Mu memohon jamuan-Mu lalu Engkau tidak menjamunya? Dan siapakah yang bersimpuh di pintu-Mu mengharap pemberian-Mu lalu Engkau tidak memberinya? Apakah pantas aku kembali dari pintu-Mu dengan kecewa dan ditolak, padahal aku tidak mengenal Tuan selain Engkau yang disifati dengan kebaikan? Bagaimana aku berharap kepada selain-Mu sedangkan segala kebaikan ada di tangan-Mu? Dan bagaimana aku menanti dari selain-Mu sedangkan penciptaan dan urusan adalah milik-Mu?

Wahai Tuhanku, bagaimana aku bisa kecewa sedangkan Engkau adalah harapanku? Atau bagaimana aku bisa dihinakan sedangkan kepada-Mu-lah sandaranku? Atau bagaimana aku bisa menjadi rendah sedangkan dengan-Mu adalah kemuliaanku? Bagaimana aku bisa dizalimi sedangkan Engkau adalah Penolongku? Atau bagaimana aku bisa tersia-sia sedangkan Engkau adalah Penjagaku? Atau bagaimana aku bisa sesat sedangkan Engkau adalah Petunjukku? Atau bagaimana aku bisa fakir sedangkan Engkau adalah Kekayaanku? Bagaimana aku merasa kesepian sedangkan Engkau adalah Penghiburku? Bagaimana aku bisa tergelincir sedangkan Engkau adalah Pemaafku? Bagaimana aku bisa terlantar sedangkan Engkau adalah Pembelaku? Bagaimana aku bisa hina sedangkan dari-Mu adalah kemuliaanku? Bagaimana aku bisa butuh sedangkan kepada-Mu tempat kembaliku? Bagaimana aku bisa sesat sedangkan Engkau adalah Pemberi petunjukku? Bagaimana aku bisa dizalimi sedangkan Engkau adalah Pembelaku? Bagaimana aku bisa dikalahkan sedangkan Engkau adalah Penolongku? Bagaimana aku bisa lalai dari-Mu sedangkan Engkau adalah Pengawasku?

Wahai Tuhanku, pada ujung kedermawanan-Mu aku gantungkan tanganku, dan untuk memperoleh pemberian-Mu aku bentangkan harapanku. Maka murnikanlah aku dengan kemurnian tauhid-Mu, dan jadikan aku termasuk hamba-hamba pilihan-Mu. Wahai Dzat yang kepada-Nya berlindung setiap orang yang lari, dan yang diharapkan oleh setiap pencari. Wahai sebaik-baik yang diharapkan, wahai semulia-mulia yang diseru, wahai Dzat yang tidak ditolak peminta-Nya, dan tidak dikecewakan pengharap-Nya. Wahai Dzat yang pintu-Nya terbuka bagi penyeru-Nya, dan hijab-Nya terangkat bagi pengharap-Nya. Aku memohon kepada-Mu dengan kedermawanan-Mu agar Engkau anugerahkan kepadaku dari pemberian-Mu apa yang menyejukkan mataku, dan dari harapan-Mu apa yang menenangkan jiwaku, dan dari keyakinan apa yang meringankan musibah dunia bagiku, dan menyingkap penutup kebutaan dari mata hatiku, dengan rahmat-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_shakirin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, terus-menerusnya karunia-Mu telah melalaikanku dari melaksanakan syukur kepada-Mu, dan limpahan keutamaan-Mu telah membuatku lemah untuk menghitung pujian kepada-Mu, dan silih bergantinya pemberian-Mu telah menyibukkanku dari menyebutkan kebaikan-kebaikan-Mu, dan berturut-turutnya nikmat-Mu telah melelahkanku dari menyebarkan kemurahan-Mu. Ini adalah kedudukan orang yang mengakui melimpahnya nikmat, dan membalasnya dengan kekurangan, dan bersaksi atas dirinya dengan kelalaian dan penyia-nyiaan, sedangkan Engkau adalah Yang Maha Santun lagi Maha Penyayang, Yang Maha Baik lagi Maha Mulia, yang tidak mengecewakan orang yang menuju kepada-Nya, dan tidak mengusir dari halaman-Nya orang yang berharap kepada-Nya.

Wahai Tuhanku, syukurku menjadi kecil di hadapan besarnya nikmat-nikmat-Mu, dan pujianku menjadi kerdil di samping pemuliaan-Mu kepadaku, dan sanjunganku jauh dari mencapai sekurang-kurangnya syukur kepada-Mu, dan hitunganku gagal untuk menjangkau puncak penganugerahan-Mu.

Wahai Tuhanku, jika umurku panjang dalam kemaksiatan kepada-Mu, dan dosaku besar dalam catatan amal, namun aku tidak mengharapkan selain ampunan-Mu, dan aku tidak menanti selain keridhaan-Mu, dan aku tidak berlindung kepada selain maaf-Mu, dan aku tidak memohon pertolongan kepada selain pertolongan-Mu. Engkau adalah Pemilik apa yang Engkau kuasakan kepadaku, dan Yang Berkuasa atas apa yang Engkau mampukan aku. Maka kekuatan apa yang Engkau berikan kepadaku, janganlah Engkau cabut; dan apa yang Engkau anugerahkan kepadaku dari kedermawanan-Mu, janganlah Engkau ambil; dan apa yang Engkau tutupi atasku dengan kesantunan-Mu, janganlah Engkau singkap; dan apa yang Engkau ketahui dari buruknya perbuatanku, ampunilah.

Wahai Tuhanku, sebagaimana Engkau telah memberi makan kami dengan kelembutan-Mu, dan memelihara kami dengan perbuatan-Mu, maka sempurnakanlah bagi kami nikmat-nikmat yang melimpah, dan tolaklah dari kami bencana-bencana yang tidak disukai, dan berikanlah kepada kami bagian yang tertinggi dan teragung dari dua negeri (dunia dan akhirat), segera maupun tertunda. Bagi-Mu segala puji atas baiknya ujian-Mu dan melimpahnya nikmat-Mu, pujian yang sesuai dengan keridhaan-Mu, dan menarik kebaikan dan kedermawanan-Mu yang besar, wahai Yang Maha Agung, wahai Yang Maha Mulia, dengan rahmat-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_mutiin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, ilhamkanlah kepada kami ketaatan kepada-Mu dan jauhkanlah kami dari kemaksiatan kepada-Mu, dan mudahkanlah bagi kami mencapai apa yang kami harapkan berupa keridhaan-Mu, dan tempatkanlah kami di tengah-tengah surga-Mu, dan singkirkanlah dari pandangan hati kami awan keraguan, dan bukalah dari hati kami penutup kebimbangan dan hijab, dan lenyapkanlah kebatilan dari nurani kami, dan tetapkanlah kebenaran dalam rahasia hati kami. Karena keraguan dan prasangka adalah pembuahan fitnah, dan pengeruh kejernihan pemberian dan anugerah.

Wahai Allah, bawalah kami dalam perahu keselamatan-Mu, dan berilah kami kenikmatan dengan lezatnya bermunajat kepada-Mu, dan bawalah kami ke telaga cinta-Mu, dan rasakanlah kepada kami manisnya kasih sayang dan kedekatan-Mu. Jadikanlah perjuangan kami di jalan-Mu, dan cita-cita kami dalam ketaatan kepada-Mu, dan murnikanlah niat kami dalam bermuamalah dengan-Mu. Karena kami ada dengan-Mu dan untuk-Mu, dan tidak ada perantara bagi kami kepada-Mu kecuali dengan-Mu.

Wahai Tuhanku, jadikanlah aku termasuk orang-orang terpilih yang baik, dan gabungkanlah aku dengan orang-orang saleh yang berbakti, yang berlomba-lomba menuju kemuliaan, yang bersegera menuju kebaikan, yang beramal untuk amal-amal saleh yang kekal, yang berusaha menuju derajat yang tinggi. Sesungguhnya Engkau Maha Kuasa atas segala sesuatu, dan pantas untuk mengabulkan, dengan rahmat-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_muridin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Mahasuci Engkau! Betapa sempitnya jalan bagi orang yang Engkau tidak menjadi petunjuknya, dan betapa jelasnya kebenaran bagi orang yang Engkau tunjuki jalannya.

Wahai Tuhanku, maka jalankanlah kami di jalan-jalan untuk sampai kepada-Mu, dan perjalankanlah kami di rute terdekat untuk datang kepada-Mu. Dekatkanlah kepada kami yang jauh, dan mudahkanlah bagi kami yang sulit dan berat. Gabungkanlah kami dengan hamba-hamba yang bersegera menuju-Mu, yang terus-menerus mengetuk pintu-Mu, yang menyembah-Mu di malam hari, dan mereka takut akan kehebatan-Mu. Mereka yang telah Engkau murnikan tempat minumnya, Engkau sampaikan keinginannya, Engkau sukseskan tujuannya, Engkau penuhi hajatnya dari hubungan dengan-Mu, Engkau penuhi hati nurani mereka dengan cinta-Mu, dan Engkau puaskan dahaga mereka dari minuman-Mu yang murni. Maka dengan-Mu mereka sampai kepada kebahagiaan kedekatan, dan dari-Mu mereka memperoleh ketenangan rasa aman, dan kepada-Mu mereka bertawakal di kedudukan kejujuran.

Wahai Tuhanku, ini adalah kedudukan orang yang cita-citanya terputus hanya kepada-Mu, dan keinginannya beralih ke arah-Mu. Maka Engkaulah, bukan selain-Mu, yang aku inginkan; dan karena-Mu, bukan karena selain-Mu, aku begadang dan tidak tidur. Bertemu dengan-Mu adalah penyejuk mataku, hubungan dengan-Mu adalah cita-cita jiwaku, kepada-Mu kerinduanku, dalam cinta-Mu adalah kegilaanku, kepada keridhaan-Mu adalah hasratku, keridhaan-Mu adalah tujuanku, melihat-Mu adalah keperluanku, bertetangga dengan-Mu adalah permintaanku, kedekatan-Mu adalah puncak pertanyaanku, dalam bermunajat dengan-Mu adalah keakraban dan ketenanganku, dan di sisi-Mu adalah obat penyakitku, penyembuh dahagaku, pendingin panas hatiku, dan penghilang kesusahanku. Maka jadilah Penghiburku dalam kesepianku, Pemaaf ketergelinciranku, Pengampun kesalahanku, Penerima tobatku, Pengabul doaku, Penolong penjagaanku, dan Pencukup kefakiranku. Janganlah Engkau putuskan aku dari-Mu, dan janganlah Engkau jauhkan aku dari-Mu, wahai Kenikmatanku dan Surgaku, wahai Duniaku dan Akhiratku.""",

    "munajat_muhibbin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, siapakah yang telah merasakan manisnya cinta-Mu lalu menginginkan pengganti selain-Mu? Dan siapakah yang telah merasa akrab dengan kedekatan-Mu lalu mencari perpindahan dari-Mu? Wahai Tuhanku, maka jadikanlah kami termasuk orang yang Engkau pilih untuk kedekatan dan kewalian-Mu, Engkau murnikan untuk kasih sayang dan cinta-Mu, Engkau rindu-kan untuk bertemu dengan-Mu, Engkau ridhai dengan ketetapan-Mu, Engkau anugerahi dengan memandang Wajah-Mu, Engkau berikan keridhaan-Mu, Engkau lindungi dari pengusiran dan kebencian-Mu, Engkau tempatkan di kedudukan kejujuran di sisi-Mu, Engkau khususkan dengan pengenalan-Mu (ma'rifat), Engkau layakkan untuk beribadah kepada-Mu, Engkau buat jatuh cinta pada kehendak-Mu, Engkau pilih untuk menyaksikan-Mu, Engkau kosongkan wajahnya untuk-Mu, Engkau luangkan hatinya untuk cinta-Mu, Engkau buat dia benci pada selain-Mu, Engkau buat dia gemar pada apa yang ada di sisi-Mu, Engkau ilhamkan zikir-Mu, Engkau bagikan syukur-Mu, Engkau sibukkan dengan ketaatan-Mu, Engkau jadikan termasuk makhluk-Mu yang saleh, Engkau pilih untuk bermunajat kepada-Mu, dan Engkau putuskan darinya segala sesuatu yang memutuskannya dari-Mu.

Wahai Allah, jadikanlah kami termasuk orang-orang yang kebiasaannya adalah bersuka ria dengan-Mu dan merindu, dan waktunya adalah mengeluh dan merintih (karena rindu). Dahi mereka bersujud karena keagungan-Mu, mata mereka begadang dalam melayani-Mu, air mata mereka mengalir karena takut kepada-Mu, hati mereka bergantung pada cinta-Mu, dan hati nurani mereka terlepas karena wibawa-Mu. Wahai Dzat yang cahaya kesucian-Nya jernih bagi pandangan para pecinta-Nya, dan keagungan Wajah-Nya menarik bagi hati orang-orang yang mengenal-Nya. Wahai cita-cita hati orang-orang yang rindu, wahai puncak harapan para pecinta. Aku memohon kepada-Mu cinta-Mu, dan cinta orang yang mencintai-Mu, dan cinta setiap amal yang menyampaikanku pada kedekatan dengan-Mu. Dan jadikanlah Engkau lebih aku cintai daripada selain-Mu, dan jadikanlah cintaku kepada-Mu sebagai pemimpin menuju keridhaan-Mu, dan kerinduanku kepada-Mu sebagai penghalang dari bermaksiat kepada-Mu. Anugerahkanlah kepadaku memandang kepada-Mu, dan pandanglah aku dengan pandangan kasih sayang dan kelembutan, janganlah Engkau palingkan Wajah-Mu dariku, dan jadikanlah aku termasuk orang-orang yang berbahagia dan beruntung di sisi-Mu, wahai Yang Maha Mengabulkan, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_raghibin_1": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, aku tidak memiliki perantara kepada-Mu kecuali kelembutan kasih sayang-Mu, dan aku tidak memiliki jalan kepada-Mu kecuali kebaikan rahmat-Mu, dan syafaat Nabi-Mu, Nabi pembawa rahmat dan penyelamat umat dari kesusahan. Maka jadikanlah keduanya sebab bagiku untuk memperoleh ampunan-Mu, dan jadikanlah keduanya penghubung bagiku untuk meraih keridhaan-Mu. Harapanku telah singgah di tanah haram kedermawanan-Mu, dan ketamakanku (akan rahmat) telah mendarat di halaman kemurahan-Mu. Maka wujudkanlah cita-citaku pada-Mu, dan akhirilah amalku dengan kebaikan, dan jadikanlah aku termasuk orang-orang pilihan-Mu yang Engkau tempatkan di tengah-tengah surga-Mu, dan Engkau dudukkan di negeri kemuliaan-Mu, dan Engkau sejukkan mata mereka dengan memandang kepada-Mu pada hari pertemuan dengan-Mu, dan Engkau wariskan kepada mereka tempat-tempat tinggal kejujuran di sisi-Mu.

Wahai Dzat yang tidak ada pendatang yang datang kepada yang lebih dermawan daripada-Nya, dan tidak ada yang bermaksud menemukan yang lebih penyayang daripada-Nya. Wahai Sebaik-baik Dzat yang menyendiri dengan orang yang sendirian, dan wahai Dzat yang paling lembut tempat berlindung orang yang terusir. Kepada luasnya maaf-Mu aku bentangkan tanganku, dan pada ujung kedermawanan-Mu aku gantungkan telapak tanganku. Maka janganlah Engkau berikan aku pengharaman (tidak diberi), dan janganlah Engkau uji aku dengan kekecewaan dan kerugian, wahai Yang Maha Mendengar doa, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_muftaqirin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, kehancuranku tidak bisa ditambal kecuali oleh kelembutan dan kasih sayang-Mu, dan kemiskinanku tidak bisa dikayakan kecuali oleh kasih dan kebaikan-Mu, dan ketakutanku tidak bisa ditenangkan kecuali oleh keamanan-Mu, dan kehinaanku tidak bisa dimuliakan kecuali oleh kekuasaan-Mu, dan cita-citaku tidak bisa disampaikan kecuali oleh karunia-Mu, dan kekuranganku tidak bisa ditutupi kecuali oleh kedermawanan-Mu, dan hajatku tidak bisa dipenuhi oleh selain-Mu, dan kesusahanku tidak bisa dihilangkan kecuali oleh rahmat-Mu, dan bahayaku tidak bisa diangkat kecuali oleh belas kasih-Mu, dan dahagaku tidak bisa didinginkan kecuali oleh hubungan dengan-Mu, dan kerinduanku tidak bisa dipadamkan kecuali oleh pertemuan dengan-Mu, dan hasratku kepada-Mu tidak bisa dibasahi kecuali oleh memandang Wajah-Mu, dan ketenanganku tidak akan menetap tanpa kedekatanku dengan-Mu.

Dan kesedihanku tidak bisa ditolak kecuali oleh ketenteraman dari-Mu, dan penyakitku tidak bisa disembuhkan kecuali oleh pengobatan-Mu, dan kegundahanku tidak bisa dihilangkan kecuali oleh kedekatan-Mu, dan lukaku tidak bisa disembuhkan kecuali oleh maaf-Mu, dan noda hatiku tidak bisa dibersihkan kecuali oleh ampunan-Mu, dan waswas dadaku tidak bisa dihilangkan kecuali oleh perintah-Mu.

Wahai Puncak harapan orang-orang yang berharap, wahai Tujuan permintaan orang-orang yang meminta, wahai Akhir pencarian orang-orang yang mencari, wahai Tertinggi keinginan orang-orang yang berkeinginan. Wahai Pelindung orang-orang saleh, wahai Keamanan orang-orang yang takut, wahai Pengabul doa orang-orang yang dalam kesulitan, wahai Simpanan orang-orang yang tidak punya, wahai Harta orang-orang yang sengsara, wahai Penolong orang-orang yang meminta pertolongan, wahai Pemusi hajat orang-orang fakir dan miskin, wahai Yang Paling Dermawan di antara yang dermawan, wahai Yang Paling Penyayang di antara para penyayang. Kepada-Mu ketundukanku dan permintaanku, dan kepada-Mu permohonan dan ibtihalku. Aku memohon kepada-Mu agar Engkau memberiku ketenteraman keridhaan-Mu, dan mengekalkan nikmat anugerah-Mu atasku. Dan inilah aku berdiri di pintu kedermawanan-Mu, dan menghadapkan diri pada hembusan kebaikan-Mu, dan berpegang teguh pada tali-Mu yang kuat, dan bergantung pada ikatan-Mu yang kokoh.

Wahai Tuhanku, rahmatilah hamba-Mu yang hina, yang lusuh lidahnya dan sedikit amalnya. Anugerahilah dia dengan kedermawanan-Mu yang besar, dan lindungilah dia di bawah naungan-Mu yang teduh, wahai Yang Maha Mulia, wahai Yang Maha Indah, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_arifin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, lidah-lidah telah pendek untuk mencapai pujian kepada-Mu sebagaimana yang layak bagi keagungan-Mu, dan akal-akal telah lemah untuk memahami hakikat keindahan-Mu, dan mata-mata telah lelah sebelum memandang kemuliaan Wajah-Mu. Dan Engkau tidak menjadikan jalan bagi makhluk untuk mengenal-Mu kecuali melalui ketidakmampuan untuk mengenal-Mu.

Wahai Tuhanku, maka jadikanlah kami termasuk orang-orang yang pohon-pohon kerinduan kepada-Mu telah berakar di taman-taman dada mereka, dan api cinta-Mu telah menguasai seluruh hati mereka. Maka mereka berlindung ke sarang-sarang pemikiran, dan gembala di kebun-kebun kedekatan dan penyingkapan, dan meminum dari telaga cinta dengan gelas kelembutan, dan mendatangi syariat persahabatan murni. Penutup telah diangkat dari pandangan mereka, kegelapan keraguan telah hilang dari keyakinan dan nurani mereka, geljolak keraguan telah sirna dari hati dan rahasia mereka, dada mereka telah lapang dengan realisasi ma'rifat, semangat mereka telah tinggi karena mendahului kebahagiaan dalam kezuhudan, minuman mereka menjadi manis di mata air muamalah, rahasia mereka menjadi baik di majelis keakraban, kawanan mereka merasa aman di tempat ketakutan, jiwa mereka menjadi tenang dengan kembali kepada Tuhan segala tuhan, roh mereka yakin akan kemenangan dan kejayaan, mata mereka sejuk dengan memandang Kekasih mereka, ketetapan mereka menjadi tetap dengan menyadari permintaan dan meraih harapan, dan perdagangan mereka beruntung dalam menjual dunia dengan akhirat.

Wahai Tuhanku, betapa lezatnya lintasan ilham dengan mengingat-Mu pada hati, dan betapa manisnya perjalanan menuju-Mu dengan imajinasi di jalan-jalan gaib, dan betapa baiknya rasa cinta-Mu, dan betapa segarnya minuman kedekatan-Mu. Maka lindungilah kami dari pengusiran dan penjauhan-Mu, dan jadikanlah kami termasuk orang-orang yang paling khusus mengenal-Mu, hamba-hamba-Mu yang paling saleh, orang-orang yang paling jujur menaati-Mu, dan hamba-hamba-Mu yang paling ikhlas. Wahai Yang Maha Agung, wahai Yang Maha Mulia, wahai Yang Maha Dermawan, wahai Yang Maha Pemberi, dengan rahmat dan anugerah-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_dhakirin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, jikalau bukan karena kewajiban menerima perintah-Mu, niscaya aku akan mensucikan-Mu dari penyebutanku akan Dikau, karena penyebutanku akan Dikau adalah sebatas kemampuanku, bukan sebatas kemampuan-Mu. Dan berapakah nilaiku sehingga aku dijadikan tempat untuk mensucikan-Mu? Dan di antara nikmat terbesar atas kami adalah berjalannya zikir-Mu di atas lidah-lidah kami, dan izin-Mu bagi kami untuk berdoa kepada-Mu, mensucikan-Mu, dan bertasbih kepada-Mu.

Wahai Tuhanku, maka ilhamkanlah kepada kami zikir kepada-Mu dalam kesunyian dan keramaian, malam dan siang, terang-terangan dan rahasia, dalam kesenangan dan kesusahan. Akrabkanlah kami dengan zikir yang tersembunyi, pekerjakanlah kami dengan amal yang suci dan usaha yang diridhai, dan balaslah kami dengan timbangan yang penuh.

Wahai Tuhanku, hati-hati yang bingung (karena cinta) menjadi gila dengan-Mu, dan akal-akal yang berbeda bersatu atas pengenalan terhadap-Mu. Maka hati tidak menjadi tenang kecuali dengan mengingat-Mu, dan jiwa tidak menjadi tenteram kecuali saat melihat-Mu. Engkau adalah Yang Disucikan di setiap tempat, Yang Disembah di setiap zaman, Yang Ada di setiap waktu, Yang Diseru dengan setiap lisan, dan Yang Diagungkan di setiap hati. Aku memohon ampun kepada-Mu dari setiap kelezatan selain zikir-Mu, dan dari setiap kenyamanan selain keakraban dengan-Mu, dan dari setiap kegembiraan selain kedekatan dengan-Mu, dan dari setiap kesibukan selain ketaatan kepada-Mu.

Wahai Tuhanku, Engkau telah berfirman dan perkataan-Mu adalah Benar: "Wahai orang-orang yang beriman, berzikirlah (ingatlah) kepada Allah dengan zikir yang sebanyak-banyaknya. Dan bertasbihlah kepada-Nya di waktu pagi dan petang." Dan Engkau berfirman dan perkataan-Mu adalah Benar: "Maka ingatlah kamu kepada-Ku, niscaya Aku ingat (pula) kepadamu." Engkau memerintahkan kami untuk mengingat-Mu, dan menjanjikan kami atasnya bahwa Engkau akan mengingat kami, sebagai pemuliaan, pengagungan, dan pembesaran bagi kami. Dan inilah kami mengingat-Mu sebagaimana yang Engkau perintahkan, maka penuhilah bagi kami apa yang Engkau janjikan, wahai Yang Mengingat orang-orang yang berzikir, dan wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_mutawassilin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Allah, wahai Perlindungan orang-orang yang berlindung, wahai Tempat bernaung orang-orang yang mencari naungan, wahai Penyelamat orang-orang yang binasa, wahai Penjaga orang-orang yang sengsara, wahai Penyayang orang-orang miskin, wahai Pengabul doa orang-orang yang terdesak, wahai Simpanan orang-orang yang sangat butuh, wahai Penambal orang-orang yang patah hati, wahai Tempat kembali orang-orang yang terputus, wahai Penolong orang-orang yang lemah, wahai Pelindung orang-orang yang takut, wahai Penolong orang-orang yang kesusahan, wahai Benteng orang-orang yang mengungsi.

Jika aku tidak berlindung dengan kemuliaan-Mu, maka kepada siapa aku berlindung? Dan jika aku tidak bernaung dengan kekuasaan-Mu, maka kepada siapa aku bernaung?

Dosa-dosa telah memaksaku untuk bergantung pada ujung maaf-Mu, dan kesalahan-kesalahan telah membuatku butuh untuk memohon pembukaan pintu-pintu ampunan-Mu, dan keburukan telah mengundangku untuk bersimpuh di halaman kemuliaan-Mu, dan ketakutan akan siksa-Mu telah membawaku untuk berpegang pada tali kasih sayang-Mu. Tidaklah pantas bagi orang yang berpegang teguh pada tali-Mu untuk ditelantarkan, dan tidak layak bagi orang yang mencari perlindungan dengan kemuliaan-Mu untuk diserahkan atau diabaikan.

Wahai Tuhanku, maka janganlah Engkau biarkan kami tanpa perlindungan-Mu, dan janganlah Engkau telanjangi kami dari pemeliharaan-Mu, dan lindungilah kami dari jalan-jalan kebinasaan, karena kami berada dalam penglihatan-Mu dan dalam jaminan-Mu. Aku memohon kepada-Mu demi orang-orang khusus-Mu dari kalangan malaikat-Mu, dan orang-orang saleh dari makhluk-Mu, agar Engkau menjadikan bagi kami pelindung yang menyelamatkan kami dari kebinasaan, menjauhkan kami dari bencana, dan menyembunyikan kami dari musibah yang dahsyat. Dan agar Engkau menurunkan ketenangan-Mu kepada kami, dan meliputi wajah kami dengan cahaya cinta-Mu, dan menempatkan kami pada tiang-Mu yang kokoh, dan mengumpulkan kami dalam sayap perlindungan-Mu, dengan belas kasih dan rahmat-Mu, wahai Yang Paling Penyayang di antara para penyayang.""",

    "munajat_zahidin": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.

Wahai Tuhanku, Engkau telah menempatkan kami di sebuah negeri (dunia) yang telah menggali lubang tipu dayanya bagi kami, dan menggantung kami dengan tangan-tangan kematian dalam jerat pengkhianatannya. Maka kepada-Mu kami berlindung dari tipu muslihatnya, dan dengan-Mu kami berpegang teguh dari tertipu oleh hiasan indahnya. Karena ia adalah pembinasa para pencarinya, perusak para penghuninya, penuh dengan bencana, sarat dengan malapetaka.

Wahai Tuhanku, maka jadikanlah kami zuhud terhadapnya, dan selamatkanlah kami darinya dengan taufik dan perlindungan-Mu. Lepaskanlah dari kami jubah kemaksiatan kepada-Mu, uruslah urusan kami dengan kecukupan-Mu yang baik, perbanyaklah tambahan kami dari luasnya rahmat-Mu, indahkanlah pemberian kami dari limpahan anugerah-Mu, tanamkanlah di hati kami pohon-pohon cinta-Mu, sempurnakanlah bagi kami cahaya ma'rifat-Mu, rasakanlah kepada kami manisnya maaf-Mu dan lezatnya ampunan-Mu, sejukkanlah mata kami pada hari pertemuan dengan-Mu dengan memandang-Mu, dan keluarkanlah cinta dunia dari hati kami, sebagaimana Engkau perbuat terhadap orang-orang saleh dari pilihan-Mu dan orang-orang berbakti dari kekasih-Mu, dengan rahmat-Mu wahai Yang Paling Penyayang di antara para penyayang, dan wahai Yang Paling Dermawan di antara para dermawan."""
}

# --- HISN AL-MUSLIM (Bilingual: Arabic + Indonesian) ---
# Title MUST be translated.
hisn_cat_map = {
    "hisn_morning": "Dzikir Pagi",
    "hisn_evening": "Dzikir Petang",
    "hisn_sleep": "Dzikir Tidur",
    "hisn_prayer": "Dzikir Sholat",
    "hisn_food": "Dzikir Makanan",
    "hisn_travel": "Dzikir Safar",
    "hisn_mosque": "Dzikir Masjid"
}

# Format: "Translation Text... Virtue: Virtue Text..."
# Or adjust script to accept tuple ("Translation", "Virtue")
hisn_translations = {
    # --- Categories ---
    # These are handled by hisn_cat_map, but good to have context.
    
    # --- MORNING ---
    "dhikr_hisn_morning_1": """Aku berlindung kepada Allah dari godaan syetan yang terkutuk.
Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Allah, tidak ada Tuhan (yang berhak disembah) melainkan Dia Yang Hidup kekal lagi terus menerus mengurus (makhluk-Nya); tidak mengantuk dan tidak tidur. Kepunyaan-Nya apa yang di langit dan di bumi. Tiada yang dapat memberi syafa'at di sisi Allah tanpa izin-Nya? Allah mengetahui apa-apa yang di hadapan mereka dan di belakang mereka, dan mereka tidak mengetahui apa-apa dari ilmu Allah melainkan apa yang dikehendaki-Nya. Kursi Allah meliputi langit dan bumi. Dan Allah tidak merasa berat memelihara keduanya, dan Allah Maha Tinggi lagi Maha Besar.
Keutamaan: Barangsiapa membacanya ketika pagi, ia akan dilindungi dari jin hingga sore. Dan barangsiapa membacanya ketika sore, ia akan dilindungi dari jin hingga pagi.""",
    
    "dhikr_hisn_morning_2": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Katakanlah: Dialah Allah, Yang Maha Esa. Allah adalah Tuhan yang bergantung kepada-Nya segala sesuatu. Dia tiada beranak dan tidak pula diperanakkan, dan tidak ada seorangpun yang setara dengan Dia.
Keutamaan: Barangsiapa membacanya tiga kali di pagi dan sore hari, maka itu akan mencukupinya dari segala sesuatu.""",

    "dhikr_hisn_morning_3": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Katakanlah: Aku berlindung kepada Tuhan Yang Menguasai subuh, dari kejahatan makhluk-Nya, dan dari kejahatan malam apabila telah gelap gulita, dan dari kejahatan wanita-wanita tukang sihir yang menghembus pada buhul-buhul, dan dari kejahatan pendengki bila ia dengki.
Keutamaan: Barangsiapa membacanya tiga kali di pagi dan sore hari, maka itu akan mencukupinya dari segala sesuatu.""",

    "dhikr_hisn_morning_4": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Katakanlah: Aku berlindung kepada Tuhan (yang memelihara dan menguasai) manusia. Raja manusia. Sembahan manusia. Dari kejahatan (bisikan) syaitan yang biasa bersembunyi, yang membisikkan (kejahatan) ke dalam dada manusia, dari (golongan) jin dan manusia.
Keutamaan: Barangsiapa membacanya tiga kali di pagi dan sore hari, maka itu akan mencukupinya dari segala sesuatu.""",

    "dhikr_hisn_morning_5": """Kami telah memasuki waktu pagi dan kerajaan hanya milik Allah, segala puji bagi Allah. Tidak ada Tuhan (yang berhak disembah) kecuali Allah semata, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya pujian. Dialah Yang Mahakuasa atas segala sesuatu. Wahai Tuhanku, aku mohon kepada-Mu kebaikan hari ini dan kebaikan setelahnya. Aku berlindung kepada-Mu dari kejahatan hari ini dan kejahatan setelahnya. Wahai Tuhanku, aku berlindung kepada-Mu dari kemalasan dan kejelekan di hari tua. Wahai Tuhanku, aku berlindung kepada-Mu dari siksaan di neraka dan siksaan di alam kubur.""",

    "dhikr_hisn_morning_6": """Ya Allah, dengan rahmat dan pertolongan-Mu kami memasuki waktu pagi, dan dengan rahmat dan pertolongan-Mu kami memasuki waktu sore. Dengan rahmat dan pertolongan-Mu kami hidup dan dengan kehendak-Mu kami mati. Dan kepada-Mu kebangkitan (bagi semua makhluk).""",

    "dhikr_hisn_morning_7": """Ya Allah, Engkau adalah Tuhanku, tidak ada Tuhan yang berhak disembah kecuali Engkau, Engkaulah yang menciptakan aku. Aku adalah hamba-Mu. Aku akan setia pada perjanjianku dengan-Mu semampuku. Aku berlindung kepada-Mu dari kejelekan yang kuperbuat. Aku mengakui nikmat-Mu kepadaku dan aku mengakui dosaku, oleh karena itu, ampunilah aku. Sesungguhnya tiada yang dapat mengampuni dosa kecuali Engkau.
Keutamaan: Barangsiapa mengucapkannya dengan yakin di sore hari lalu ia meninggal pada malam itu, niscaya ia masuk surga. Demikian juga apabila membacanya di pagi hari.""",

    "dhikr_hisn_morning_8": """Ya Allah, sesungguhnya aku di waktu pagi ini mempersaksikan Engkau, malaikat yang memikul 'Arsy-Mu, malaikat-malaikat dan seluruh makhluk-Mu, bahwa sesungguhnya Engkau adalah Allah, tidak ada Tuhan yang berhak disembah kecuali Engkau semata, tidak ada sekutu bagi-Mu dan sesungguhnya Muhammad adalah hamba dan utusan-Mu.
Keutamaan: Barangsiapa membacanya 4 kali di pagi/sore hari, Allah membebaskannya dari api neraka.""",

    "dhikr_hisn_morning_9": """Ya Allah, nikmat yang kuterima atau diterima oleh seseorang di antara makhluk-Mu di pagi ini adalah dari-Mu semata, tidak ada sekutu bagi-Mu. Bagi-Mu segala puji dan kepada-Mu panjatan syukur.
Keutamaan: Barangsiapa membacanya di pagi hari, maka ia telah menunaikan syukurnya pada hari itu.""",

    "dhikr_hisn_morning_10": """Ya Allah, selamatkanlah tubuhku (dari penyakit dan yang tidak aku inginkan). Ya Allah, selamatkanlah pendengaranku. Ya Allah, selamatkanlah penglihatanku, tidak ada Tuhan (yang berhak disembah) kecuali Engkau. Ya Allah, sesungguhnya aku berlindung kepada-Mu dari kekufuran dan kefakiran. Aku berlindung kepada-Mu dari siksa kubur, tidak ada Tuhan (yang berhak disembah) kecuali Engkau.""",

    "dhikr_hisn_morning_11": """Cukuplah Allah bagiku; tidak ada Tuhan (yang berhak disembah) kecuali Dia. Hanya kepada-Nya aku bertawakkal dan Dia adalah Tuhan yang memiliki 'Arsy yang agung.
Keutamaan: Barangsiapa membacanya 7 kali di pagi dan sore, Allah akan mencukupkan apa yang mementingkannya (dari perkara dunia dan akhirat).""",

    "dhikr_hisn_morning_12": """Dengan nama Allah yang bila disebut, segala sesuatu di bumi dan langit tidak akan berbahaya, Dia-lah Yang Maha Mendengar lagi Maha Mengetahui.
Keutamaan: Barangsiapa membacanya 3 kali di pagi dan sore hari, tidak akan ada sesuatu pun yang membahayakannya.""",

    "dhikr_hisn_morning_13": """Aku ridha Allah sebagai Rabb, Islam sebagai agama dan Muhammad shallallahu 'alaihi wa sallam sebagai Nabi.
Keutamaan: Barangsiapa membacanya 3 kali di pagi dan sore hari, maka hak Allah untuk meridhainya pada hari kiamat.""",

    "dhikr_hisn_morning_14": """Wahai Yang Maha Hidup, wahai Yang Maha Berdiri Sendiri (mengurusi makhluk-Nya), dengan rahmat-Mu aku memohon pertolongan, perbaikilah urusanku semuanya dan janganlah Engkau serahkan aku kepada diriku sendiri sekejap mata pun.""",

    "dhikr_hisn_morning_15": """Di waktu pagi kami memegang agama Islam, kalimat ikhlas (kalimat syahadat), agama Nabi kami Muhammad shallallahu 'alaihi wa sallam, dan agama bapak kami Ibrahim, yang berdiri di atas jalan yang lurus, muslim dan tidak tergolong orang-orang musyrik.""",

    "dhikr_hisn_morning_16": """Maha Suci Allah dan segala puji bagi-Nya.
Keutamaan: Barangsiapa membacanya 100 kali dalam sehari, maka dosa-dosanya akan dihapus meskipun sebanyak buih di lautan.""",

    "dhikr_hisn_morning_17": """Tidak ada Tuhan (yang berhak disembah) kecuali Allah semata, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya pujian. Dialah Yang Mahakuasa atas segala sesuatu.
Keutamaan: Barangsiapa membacanya 100 kali di pagi hari, pahalanya seperti membebaskan 10 budak, dicatat 100 kebaikan, dihapus 100 keburukan, dan menjadi pelindung dari syetan.""",

    "dhikr_hisn_morning_18": """Maha Suci Allah dan segala puji bagi-Nya, sebanyak bilangan makhluk-Nya, dan sebesar ridha diri-Nya, dan seberat 'Arsy-Nya, dan sebanyak tinta kalimat-Nya.""",

    "dhikr_hisn_morning_19": """Ya Allah, sesungguhnya aku memohon kepada-Mu ilmu yang bermanfaat, rezeki yang baik dan amal yang diterima.""",

    "dhikr_hisn_morning_20": """Aku memohon ampun kepada Allah dan bertobat kepada-Nya.
Keutamaan: Dibaca 100 kali dalam sehari.""",

    "dhikr_hisn_morning_21": """Ya Allah, limpahkanlah shalawat dan salam serta keberkahan kepada Nabi kami Muhammad.
Keutamaan: Barangsiapa bershalawat kepadaku 10 kali di pagi hari dan 10 kali di sore hari, ia akan mendapatkan syafa'atku pada hari kiamat.""",

    # --- EVENING ---
    "dhikr_hisn_evening_1": """Aku berlindung kepada Allah dari godaan syetan yang terkutuk.
Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Allah, tidak ada Tuhan (yang berhak disembah) melainkan Dia Yang Hidup kekal lagi terus menerus mengurus (makhluk-Nya); tidak mengantuk dan tidak tidur. Kepunyaan-Nya apa yang di langit dan di bumi. Tiada yang dapat memberi syafa'at di sisi Allah tanpa izin-Nya? Allah mengetahui apa-apa yang di hadapan mereka dan di belakang mereka, dan mereka tidak mengetahui apa-apa dari ilmu Allah melainkan apa yang dikehendaki-Nya. Kursi Allah meliputi langit dan bumi. Dan Allah tidak merasa berat memelihara keduanya, dan Allah Maha Tinggi lagi Maha Besar.
Keutamaan: Barangsiapa membacanya ketika pagi, ia akan dilindungi dari jin hingga sore. Dan barangsiapa membacanya ketika sore, ia akan dilindungi dari jin hingga pagi.""",

    "dhikr_hisn_evening_2": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Katakanlah: Dialah Allah, Yang Maha Esa. Allah adalah Tuhan yang bergantung kepada-Nya segala sesuatu. Dia tiada beranak dan tidak pula diperanakkan, dan tidak ada seorangpun yang setara dengan Dia.
Keutamaan: Barangsiapa membacanya tiga kali di pagi dan sore hari, maka itu akan mencukupinya dari segala sesuatu.""",

    "dhikr_hisn_evening_3": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Katakanlah: Aku berlindung kepada Tuhan Yang Menguasai subuh, dari kejahatan makhluk-Nya, dan dari kejahatan malam apabila telah gelap gulita, dan dari kejahatan wanita-wanita tukang sihir yang menghembus pada buhul-buhul, dan dari kejahatan pendengki bila ia dengki.
Keutamaan: Barangsiapa membacanya tiga kali di pagi dan sore hari, maka itu akan mencukupinya dari segala sesuatu.""",

    "dhikr_hisn_evening_4": """Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.
Katakanlah: Aku berlindung kepada Tuhan (yang memelihara dan menguasai) manusia. Raja manusia. Sembahan manusia. Dari kejahatan (bisikan) syaitan yang biasa bersembunyi, yang membisikkan (kejahatan) ke dalam dada manusia, dari (golongan) jin dan manusia.
Keutamaan: Barangsiapa membacanya tiga kali di pagi dan sore hari, maka itu akan mencukupinya dari segala sesuatu.""",

    "dhikr_hisn_evening_5": """Kami telah memasuki waktu sore dan kerajaan hanya milik Allah, segala puji bagi Allah. Tidak ada Tuhan (yang berhak disembah) kecuali Allah semata, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya pujian. Dialah Yang Mahakuasa atas segala sesuatu. Wahai Tuhanku, aku mohon kepada-Mu kebaikan malam ini dan kebaikan setelahnya. Aku berlindung kepada-Mu dari kejahatan malam ini dan kejahatan setelahnya. Wahai Tuhanku, aku berlindung kepada-Mu dari kemalasan dan kejelekan di hari tua. Wahai Tuhanku, aku berlindung kepada-Mu dari siksaan di neraka dan siksaan di alam kubur.""",

    "dhikr_hisn_evening_6": """Ya Allah, dengan rahmat dan pertolongan-Mu kami memasuki waktu sore, dan dengan rahmat dan pertolongan-Mu kami memasuki waktu pagi. Dengan rahmat dan pertolongan-Mu kami hidup dan dengan kehendak-Mu kami mati. Dan kepada-Mu tempat kembali.""",

    "dhikr_hisn_evening_7": """Ya Allah, Engkau adalah Tuhanku, tidak ada Tuhan yang berhak disembah kecuali Engkau, Engkaulah yang menciptakan aku. Aku adalah hamba-Mu. Aku akan setia pada perjanjianku dengan-Mu semampuku. Aku berlindung kepada-Mu dari kejelekan yang kuperbuat. Aku mengakui nikmat-Mu kepadaku dan aku mengakui dosaku, oleh karena itu, ampunilah aku. Sesungguhnya tiada yang dapat mengampuni dosa kecuali Engkau.
Keutamaan: Barangsiapa mengucapkannya dengan yakin di sore hari lalu ia meninggal pada malam itu, niscaya ia masuk surga. Demikian juga apabila membacanya di pagi hari.""",

    "dhikr_hisn_evening_8": """Ya Allah, sesungguhnya aku di waktu sore ini mempersaksikan Engkau, malaikat yang memikul 'Arsy-Mu, malaikat-malaikat dan seluruh makhluk-Mu, bahwa sesungguhnya Engkau adalah Allah, tidak ada Tuhan yang berhak disembah kecuali Engkau semata, tidak ada sekutu bagi-Mu dan sesungguhnya Muhammad adalah hamba dan utusan-Mu.
Keutamaan: Barangsiapa membacanya 4 kali di pagi/sore hari, Allah membebaskannya dari api neraka.""",

    "dhikr_hisn_evening_9": """Ya Allah, nikmat yang kuterima atau diterima oleh seseorang di antara makhluk-Mu di sore ini adalah dari-Mu semata, tidak ada sekutu bagi-Mu. Bagi-Mu segala puji dan kepada-Mu panjatan syukur.
Keutamaan: Barangsiapa membacanya di sore hari, maka ia telah menunaikan syukurnya pada malam itu.""",

    "dhikr_hisn_evening_10": """Ya Allah, selamatkanlah tubuhku (dari penyakit dan yang tidak aku inginkan). Ya Allah, selamatkanlah pendengaranku. Ya Allah, selamatkanlah penglihatanku, tidak ada Tuhan (yang berhak disembah) kecuali Engkau. Ya Allah, sesungguhnya aku berlindung kepada-Mu dari kekufuran dan kefakiran. Aku berlindung kepada-Mu dari siksa kubur, tidak ada Tuhan (yang berhak disembah) kecuali Engkau.""",

    "dhikr_hisn_evening_11": """Cukuplah Allah bagiku; tidak ada Tuhan (yang berhak disembah) kecuali Dia. Hanya kepada-Nya aku bertawakkal dan Dia adalah Tuhan yang memiliki 'Arsy yang agung.
Keutamaan: Barangsiapa membacanya 7 kali di pagi dan sore, Allah akan mencukupkan apa yang mementingkannya (dari perkara dunia dan akhirat).""",

    "dhikr_hisn_evening_12": """Dengan nama Allah yang bila disebut, segala sesuatu di bumi dan langit tidak akan berbahaya, Dia-lah Yang Maha Mendengar lagi Maha Mengetahui.
Keutamaan: Barangsiapa membacanya 3 kali di pagi dan sore hari, tidak akan ada sesuatu pun yang membahayakannya.""",

    "dhikr_hisn_evening_13": """Aku ridha Allah sebagai Rabb, Islam sebagai agama dan Muhammad shallallahu 'alaihi wa sallam sebagai Nabi.
Keutamaan: Barangsiapa membacanya 3 kali di pagi dan sore hari, maka hak Allah untuk meridhainya pada hari kiamat.""",

    "dhikr_hisn_evening_14": """Wahai Yang Maha Hidup, wahai Yang Maha Berdiri Sendiri (mengurusi makhluk-Nya), dengan rahmat-Mu aku memohon pertolongan, perbaikilah urusanku semuanya dan janganlah Engkau serahkan aku kepada diriku sendiri sekejap mata pun.""",

    "dhikr_hisn_evening_15": """Di waktu sore kami memegang agama Islam, kalimat ikhlas (kalimat syahadat), agama Nabi kami Muhammad shallallahu 'alaihi wa sallam, dan agama bapak kami Ibrahim, yang berdiri di atas jalan yang lurus, muslim dan tidak tergolong orang-orang musyrik.""",

    "dhikr_hisn_evening_16": """Maha Suci Allah dan segala puji bagi-Nya.
Keutamaan: Barangsiapa membacanya 100 kali dalam sehari, maka dosa-dosanya akan dihapus meskipun sebanyak buih di lautan.""",

    "dhikr_hisn_evening_17": """Tidak ada Tuhan (yang berhak disembah) kecuali Allah semata, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya pujian. Dialah Yang Mahakuasa atas segala sesuatu.
Keutamaan: Barangsiapa membacanya 100 kali di pagi hari, pahalanya seperti membebaskan 10 budak, dicatat 100 kebaikan, dihapus 100 keburukan, dan menjadi pelindung dari syetan.""",

    "dhikr_hisn_evening_18": """Aku berlindung dengan kalimat-kalimat Allah yang sempurna dari kejahatan makhluk yang diciptakan-Nya.
Keutamaan: Barangsiapa membacanya di sore hari, niscaya tidak akan ada racun yang membahayakannya malam itu.""",

    "dhikr_hisn_evening_19": """Ya Allah, limpahkanlah shalawat dan salam serta keberkahan kepada Nabi kami Muhammad.
Keutamaan: Barangsiapa bershalawat kepadaku 10 kali di pagi hari dan 10 kali di sore hari, ia akan mendapatkan syafa'atku pada hari kiamat.""",

    # --- SLEEP ---
    "dhikr_hisn_sleep_1": """Membaca Surat Al-Ikhlas, Al-Falaq, dan An-Naas.
Keutamaan: Disunnahkan mengumpulkan dua telapak tangan lalu meniupnya dan membaca Al-Ikhlas, Al-Falaq, dan An-Naas, kemudian mengusapkan ke tubuh semampunya, dimulai dari kepala, wajah, dan tubuh bagian depan. (Diulang 3x)""",
    
    "dhikr_hisn_sleep_2": """(Lihat dhikr 1)""",
    "dhikr_hisn_sleep_3": """(Lihat dhikr 1)""",

    "dhikr_hisn_sleep_4": """Dengan nama-Mu, wahai Tuhanku, aku meletakkan lambungku. Dan dengan nama-Mu pula aku bangun daripadanya. Apabila Engkau menahan rohku (mati), maka berilah rahmat padanya. Tapi apabila Engkau melepaskannya, maka peliharalah, sebagaimana Engkau memelihara hamba-hamba-Mu yang orang-orang sâlih.""",

    "dhikr_hisn_sleep_5": """Ya Allah, sesungguhnya Engkau telah menciptakan diriku, dan Engkaulah yang akan mematikannya. Mati dan hidupnya hanya milik-Mu. Apabila Engkau menghidupkannya, maka peliharalah. Dan apabila Engkau mematikannya, maka ampunilah. Ya Allah, sesungguhnya aku memohon pada-Mu keselamatan.""",

    "dhikr_hisn_sleep_6": """Ya Allah, peliharalah aku dari azab-Mu pada hari Engkau membangkitkan hamba-hamba-Mu.
Keutamaan: Dibaca 3 kali.""",

    "dhikr_hisn_sleep_7": """Dengan nama-Mu, Ya Allah, aku mati dan aku hidup.""",

    "dhikr_hisn_sleep_8": """Maha Suci Allah (33x), Segala puji bagi Allah (33x), Allah Maha Besar (34x).
Keutamaan: Barangsiapa membacanya sebelum tidur, itu lebih baik baginya daripada seorang pembantu.""",

    # --- PRAYER ---
    "dhikr_hisn_prayer_1": """Aku minta ampun kepada Allah (3x). Ya Allah, Engkau Mahasejahtera, dan dari-Mulah kesejahteraan, Maha Suci Engkau Wahai Tuhan pemilik keagungan dan kemuliaan.""",

    "dhikr_hisn_prayer_2": """Tiada Tuhan (yang berhak disembah) kecuali Allah, Yang Maha Esa, tidak ada sekutu bagi-Nya. Bagi-Nya kerajaan dan segenap pujian. Dia-lah Yang Mahakuasa atas segala sesuatu. Ya Allah, tidak ada yang mencegah apa yang Engkau berikan dan tidak ada yang memberi apa yang Engkau cegah. Tidak berguna kekayaan dan kemuliaan itu bagi pemiliknya (selain iman dan amal shalihnya). Hanya dari-Mu kekayaan dan kemuliaan.""",

    "dhikr_hisn_prayer_3": """Maha Suci Allah (33x), Segala puji bagi Allah (33x), Allah Maha Besar (33x). Tiada Tuhan (yang berhak disembah) kecuali Allah semata, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya pujian. Dialah Yang Mahakuasa atas segala sesuatu.
Keutamaan: Barangsiapa membacanya setelah shalat, diampuni kesalahannya walaupun sebanyak buih di lautan.""",

    "dhikr_hisn_prayer_4": """Membaca Al-Ikhlas, Al-Falaq, dan An-Naas.
Keutamaan: Dibaca setiap selesai shalat (sekali), dan tiga kali setelah shalat Subuh dan Maghrib.""",

    "dhikr_hisn_prayer_5": """Membaca Ayat Kursi.
Keutamaan: Barangsiapa membacanya setiap selesai shalat fardhu, tidak ada yang menghalanginya masuk surga kecuali kematian.""",

    # --- FOOD ---
    "dhikr_hisn_food_1": """Bismillah (Dengan menyebut nama Allah).
Keutamaan: Rasulullah bersabda: Jika salah satu dari kalian makan, hendaklah menyebut nama Allah.""",

    "dhikr_hisn_food_2": """Segala puji bagi Allah yang memberi makan ini kepadaku dan memberi rezeki kepadaku tanpa daya dan kekuatan dariku.
Keutamaan: Diampuni dosanya yang telah lalu.""",

    # --- TRAVEL ---
    "dhikr_hisn_travel_1": """Allah Maha Besar (3x). Maha Suci Tuhan yang menundukkan kendaraan ini untuk kami, padahal kami sebelumnya tidak mampu menguasainya. Dan sesungguhnya kami akan kembali kepada Tuhan kami.""",

    "dhikr_hisn_travel_2": """Ya Allah, sesungguhnya kami memohon kebaikan dan takwa dalam perjalanan ini, dan amal yang Engkau ridhai. Ya Allah, mudahkanlah perjalanan ini bagi kami, dan dekatkanlah jaraknya. Ya Allah, Engkaulah teman dalam perjalanan dan pengganti dalam keluarga. Ya Allah, sesungguhnya aku berlindung kepada-Mu dari kelelahan perjalanan, pemandangan yang menyedihkan, dan perubahan yang buruk dalam harta dan keluarga.""",

    # --- MOSQUE ---
    "dhikr_hisn_mosque_1": """Aku berlindung kepada Allah Yang Maha Agung, dan dengan wajah-Nya Yang Mulia, serta kekuasaan-Nya yang azali, dari syetan yang terkutuk. Dengan nama Allah, dan shalawat serta salam semoga tercurah kepada Rasulullah. Ya Allah, bukalah pintu-pintu rahmat-Mu untukku.""",

    "dhikr_hisn_mosque_2": """Dengan nama Allah, dan shalawat serta salam semoga tercurah kepada Rasulullah. Ya Allah, sesungguhnya aku memohon keutamaan dari-Mu. Ya Allah, peliharalah aku dari godaan syetan yang terkutuk."""
}


def generate_full_content():
    print("Generating Indonesian Content...")
    
    # --- 1. DALAIL GENERATION (Monolingual) ---
    src_awrad = 'app/src/main/assets/data/awrad.json'
    if os.path.exists(src_awrad):
        with open(src_awrad, 'r', encoding='utf-8') as f:
            awrad_list = json.load(f)
        
        final_dalail = []
        for item in awrad_list:
            if item.get('type') == 'dua':
                item_id = item['id']
                
                # Fetch Indonesian data
                title_id = dalail_titles.get(item_id, item.get('title', ''))
                content_id = dalail_translations.get(item_id, "") # FULL INDONESIAN TEXT
                
                if not content_id:
                     content_id = "[Terjemahan belum tersedia]"

                final_item = {
                    "id": item_id,
                    "type": "dua",
                    "title": title_id,
                    "content": content_id, # Replaces Arabic
                    "translation": ""      # Empty
                }
                final_dalail.append(final_item)
            
        os.makedirs('app/src/main/assets/id', exist_ok=True)
        with open('app/src/main/assets/id/dalail.json', 'w', encoding='utf-8') as f:
            json.dump(final_dalail, f, ensure_ascii=False, indent=2)
        print("Generated id/dalail.json")

    # --- 2. MUNAJAT GENERATION (Monolingual) ---
    src_munajat = 'app/src/main/assets/data/munajat.json'
    if os.path.exists(src_munajat):
        with open(src_munajat, 'r', encoding='utf-8') as f:
            munajat_list = json.load(f)
        
        final_munajat = []
        for item in munajat_list:
            item_id = item['id']
            title_id = munajat_titles_id.get(item_id, item.get('title', ''))
            content_id = munajat_translations.get(item_id, "[Terjemahan belum tersedia]")

            final_item = {
                "id": item_id,
                "type": "dua",
                "title": title_id,
                "content": content_id, # Replaces Arabic
                "translation": ""      # Empty
            }
            final_munajat.append(final_item)

        with open('app/src/main/assets/id/munajat.json', 'w', encoding='utf-8') as f:
            json.dump(final_munajat, f, ensure_ascii=False, indent=2)
        print("Generated id/munajat.json")
    
    # --- 3. HISN GENERATION (Bilingual) ---
    src_hisn = 'app/src/main/assets/data/hisn.json'
    if os.path.exists(src_hisn):
        with open(src_hisn, 'r', encoding='utf-8') as f:
            structure = json.load(f)
        
        final_hisn = []
        for category in structure:
            new_cat = category.copy()
            new_cat['items'] = []
            
            # Map Category Title
            if new_cat['id'] in hisn_cat_map:
                new_cat['title'] = hisn_cat_map[new_cat['id']]

            for item in category['items']:
                item_id = item['id']
                # Try exact match first
                trans_text = hisn_translations.get(item_id, "")
                
                # If not found, try removing suffix (for IDs like 'dhikr_hisn_morning_1_12345')
                if not trans_text:
                    parts = item_id.rsplit('_', 1)
                    if len(parts) > 1 and parts[1].isdigit():
                        base_id = parts[0]
                        trans_text = hisn_translations.get(base_id, "")
                
                final_item = item.copy()
                
                # Keep Arabic in content
                if 'arabic' in item:
                    final_item['content'] = item['arabic']
                else:
                    final_item['content'] = item.get('content', '')

                # Separate Translation and Fadl
                if trans_text:
                    if "Keutamaan:" in trans_text:
                        parts = trans_text.split("Keutamaan:", 1)
                        final_item['translation'] = parts[0].strip()
                        final_item['fadl'] = parts[1].strip()
                    else:
                        final_item['translation'] = trans_text.strip()
                        final_item['fadl'] = ""
                else:
                    final_item['translation'] = ""
                    final_item['fadl'] = ""
                
                new_cat['items'].append(final_item)
            
            final_hisn.append(new_cat)

        with open('app/src/main/assets/id/hisn.json', 'w', encoding='utf-8') as f:
            json.dump(final_hisn, f, ensure_ascii=False, indent=2)
        print("Generated id/hisn.json")

    # --- 4. STATIC STRINGS ---
    static_data = {
         "app_title": "Awrad",
         "daily_wird": "Hizb Harian",
         "settings": "Pengaturan"
    }
    with open('app/src/main/assets/id/static.json', 'w', encoding='utf-8') as f:
        json.dump(static_data, f, ensure_ascii=False, indent=2)
    print("Generated id/static.json")

if __name__ == "__main__":
    generate_full_content()
