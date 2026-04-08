/**
 * ==============================================================================
 * CURHATBOX CORE JAVASCRIPT
 * Professional Standards compliant (ES6+)
 * ==============================================================================
 */

/**
 * Fungsi untuk menyalin tautan profil ke clipboard penguna.
 * Digunakan di Dashboard untuk mempermudah berbagi link Curhat.
 */
const copyToClipboard = () => {
    const copyText = document.getElementById("profileLink");
    if (copyText) {
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(copyText.value);
        
        const btn = document.getElementById("copyBtn");
        const originalText = btn.innerHTML;
        
        btn.innerHTML = "Tersalin! ✅";
        setTimeout(() => { 
            btn.innerHTML = originalText; 
        }, 2000);
    }
};

/**
 * Global timer interval untuk proses unlock HD Story.
 * @type {number|null}
 */
let hdTimerInterval = null;

/**
 * Memulai proses animasi "Unlocking HD" sebelum men-generate story.
 * Menampilkan progress bar dan timer selama 15 detik.
 * 
 * @param {string} question - Teks pertanyaan/curhatan.
 * @param {string} answer - Teks balasan.
 * @param {string} username - Nama pengguna.
 */
const startHdUnlockProcess = (question, answer, username) => {
    const modalElem = document.getElementById('hdUnlockModal');
    if (!modalElem) return;

    const modal = new bootstrap.Modal(modalElem);
    const progressBar = document.getElementById('hdProgressBar');
    const timerText = document.getElementById('hdTimerText');
    const percentText = document.getElementById('hdPercentText');
    const actionArea = document.getElementById('hdUnlockActions');
    const downloadBtn = document.getElementById('btnDownloadHD');
    
    // Reset state awal
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
        
        // Update tampilan visual
        progressBar.style.width = `${progress}%`;
        timerText.innerText = `${timeLeft}s`;
        percentText.innerText = `${Math.round(progress)}%`;
        
        if (timeLeft <= 0) {
            clearInterval(hdTimerInterval);
            timerText.innerText = 'Unlocked! ✨';
            actionArea.classList.remove('d-none');
            
            // Event listener tombol download
            downloadBtn.onclick = () => {
                modal.hide();
                generateStory(question, answer, username);
            };
        }
    }, 1000);

    // Stop timer jika user menutup modal secara manual
    modalElem.addEventListener('hidden.bs.modal', () => {
        clearInterval(hdTimerInterval);
    }, { once: true });
};

/**
 * Menghasilkan gambar (render) untuk IG Story menggunakan html2canvas.
 * Membedakan mekanisme simpan antara Desktop (auto-download) dan Mobile (preview modal).
 * 
 * @param {string} question - Teks pertanyaan.
 * @param {string} answer - Teks balasan.
 * @param {string} username - Nama pengguna.
 */
const generateStory = (question, answer, username) => {
    const qElem = document.getElementById('capture-question');
    const aElem = document.getElementById('capture-answer');
    const uElem = document.getElementById('capture-username-inner');

    if (qElem && aElem && uElem) {
        qElem.innerText = `"${question}"`;
        aElem.innerText = answer;
        uElem.innerText = username;

        const captureElement = document.getElementById('hidden-capture-area');

        // Delay sedikit untuk memastikan DOM telah ter-update sebelum render
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
                const imgData = canvas.toDataURL('image/png', 1.0);
                
                // Deteksi Device
                const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
                
                if (isMobile) {
                    // Mobile: Gunakan Preview Modal (Failsafe untuk browser seluler)
                    const previewModalElem = document.getElementById('storyPreviewModal');
                    const previewImg = document.getElementById('storyPreviewImage');
                    
                    if (previewModalElem && previewImg) {
                        previewImg.src = imgData;
                        const previewModal = new bootstrap.Modal(previewModalElem);
                        previewModal.show();
                    } else {
                        // Fallback jika modal tidak tersedia
                        window.open().document.write(`<img src="${imgData}" style="width:100%">`);
                    }
                } else {
                    // Desktop: Trigger download otomatis
                    const link = document.createElement('a');
                    link.download = `CurhatBox-Story-${Date.now()}.png`;
                    link.href = imgData;
                    link.click();
                }
            }).catch(error => {
                console.error("Gagal melakukan render gambar:", error);
                alert("Terjadi kesalahan saat membuat gambar. Silakan coba lagi.");
            });
        }, 300);
    }
};