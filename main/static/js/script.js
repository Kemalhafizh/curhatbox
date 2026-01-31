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

        // 2. Notifikasi Loading
        alert("Sedang membuat gambar untuk IG Story... Tunggu sebentar! 📸");

        // 3. Proses html2canvas
        const captureElement = document.getElementById('hidden-capture-area');

        html2canvas(captureElement, {
            scale: 1, 
            useCORS: true 
        }).then(canvas => {
            const link = document.createElement('a');
            link.download = 'curhatbox-story-' + Date.now() + '.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        }).catch(err => {
            console.error("Gagal membuat gambar:", err);
            alert("Gagal membuat gambar :( Coba lagi.");
        });
    } else {
        console.error("Elemen template IG Story tidak ditemukan.");
    }
}