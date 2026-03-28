/* =========================================
   Fungsi Salin Link (Dashboard)
   ========================================= */
function copyToClipboard() {
    var copyText = document.getElementById("profileLink");
    if (copyText) {
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(copyText.value);
        
        var btn = document.getElementById("copyBtn");
        var originalText = btn.innerHTML;
        
        btn.innerHTML = "Tersalin! ✅";
        setTimeout(() => { btn.innerHTML = "Salin"; }, 2000);
    }
}

/* =========================================
   Fungsi Generate Gambar IG Story
   ========================================= */
function generateStory(question, answer, username) {
    // 1. Masukkan data ke template tersembunyi
    var qElem = document.getElementById('capture-question');
    var aElem = document.getElementById('capture-answer');
    var uElem = document.getElementById('capture-username');

    if(qElem && aElem && uElem) {
        qElem.innerText = '"' + question + '"';
        aElem.innerText = answer;
        uElem.innerText = username;

        // 2. Proses html2canvas (High Definition 1080p Optimization)
        const captureElement = document.getElementById('hidden-capture-area');

        // Gunakan timeout sebentar agar browser sempat me-render perubahan teks/gambar
        setTimeout(() => {
            html2canvas(captureElement, {
                scale: 2, // Meningkatkan ketajaman gambar (HD+)
                useCORS: true,
                allowTaint: false,
                backgroundColor: null,
                logging: false
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'CurhatBox-Story-' + Date.now() + '.png';
                link.href = canvas.toDataURL('image/png', 1.0);
                link.click();
                console.log("Story generated successfully at 2x scale.");
            }).catch(err => {
                console.error("Gagal membuat gambar:", err);
                alert("Gagal membuat gambar :( Coba lagi.");
            });
        }, 100);
    } else {
        console.error("Elemen template IG Story tidak ditemukan.");
    }
}