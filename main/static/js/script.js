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
   Fungsi Generate Gambar IG Story (Premium HD Lock)
   ========================================= */
let hdTimerInterval = null;

function startHdUnlockProcess(question, answer, username) {
    // Ambil elemen UI Modal
    const modalElem = document.getElementById('hdUnlockModal');
    if (!modalElem) return;

    const modal = new bootstrap.Modal(modalElem);
    const progressBar = document.getElementById('hdProgressBar');
    const timerText = document.getElementById('hdTimerText');
    const percentText = document.getElementById('hdPercentText');
    const actionArea = document.getElementById('hdUnlockActions');
    const downloadBtn = document.getElementById('btnDownloadHD');
    
    // Reset UI ke keadaan awal
    progressBar.style.width = '0%';
    timerText.innerText = '15s';
    percentText.innerText = '0%';
    actionArea.classList.add('d-none');
    
    modal.show();
    
    let timeLeft = 15;
    if (hdTimerInterval) clearInterval(hdTimerInterval);
    
    hdTimerInterval = setInterval(() => {
        timeLeft--;
        const progress = ((15 - timeLeft) / 15) * 100;
        
        // Update Visual Progress
        progressBar.style.width = progress + '%';
        timerText.innerText = timeLeft + 's';
        percentText.innerText = Math.round(progress) + '%';
        
        if (timeLeft <= 0) {
            clearInterval(hdTimerInterval);
            timerText.innerText = 'Unlocked! ✨';
            actionArea.classList.remove('d-none');
            
            // Bind fungsi download ke tombol yang baru muncul
            downloadBtn.onclick = () => {
                modal.hide();
                // Panggil fungsi generator asli
                generateStory(question, answer, username);
            };
        }
    }, 1000);

    // Hentikan timer jika modal ditutup paksa (Cancel)
    modalElem.addEventListener('hidden.bs.modal', function () {
        clearInterval(hdTimerInterval);
    }, { once: true });
}

function generateStory(question, answer, username) {
    // (Fungsi generator tetap sama, hanya sekarang dipanggil via startHdUnlockProcess)
    var qElem = document.getElementById('capture-question');
    var aElem = document.getElementById('capture-answer');
    var uElem = document.getElementById('capture-username-inner');

    if(qElem && aElem && uElem) {
        qElem.innerText = '"' + question + '"';
        aElem.innerText = answer;
        uElem.innerText = username;

        const captureElement = document.getElementById('hidden-capture-area');

        setTimeout(() => {
            html2canvas(captureElement, {
                scale: 2, 
                useCORS: true,
                allowTaint: false,
                backgroundColor: null,
                logging: false,
                width: 1080,
                height: 1920
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'CurhatBox-Story-' + Date.now() + '.png';
                link.href = canvas.toDataURL('image/png', 1.0);
                link.click();
            }).catch(err => {
                console.error("Gagal membuat gambar:", err);
                alert("Gagal membuat gambar :( Coba lagi.");
            });
        }, 300); // Penambahan delay sedikit untuk stabilitas render
    }
}