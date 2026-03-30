import urllib.request
import urllib.error
import sys

ROUTES = ["/", "/about/", "/rules/", "/register/", "/login/"]
BASE_URL = "https://curhatbox.my.id"
success = True

with open("qc_log.txt", "w", encoding="utf-8") as f:
    f.write(f"Memulai Uji Backend Endpoints (QC) di {BASE_URL}...\n")
    for route in ROUTES:
        url = f"{BASE_URL}{route}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                status = response.status
                f.write(f"[PASS] GET {route} -> Status: {status}\n")
        except urllib.error.HTTPError as e:
            status = e.code
            if status in [302, 301, 403]:
                 f.write(f"[PASS/REDIRECT] GET {route} -> Status: {status}\n")
            else:
                 f.write(f"[FAIL] GET {route} -> Status: {status}\n")
                 success = False
        except urllib.error.URLError as e:
            f.write(f"[ERROR] Gagal menghubungi {url}: {e.reason}\n")
            success = False

    if success:
        f.write("QC Backend: Semua rute publik merespons dengan sehat (200/Redirect).\n")
    else:
        f.write("QC Backend: Ditemukan masalah pada beberapa rute.\n")

if not success:
    sys.exit(1)
