import re
import json
from urllib import request, parse

from django.conf import settings


def sensor_kata(teks):
    """
    Mengganti kata-kata kasar dengan tanda bintang (*).
    Mendukung Case Insensitive (Huruf besar/kecil tetap kena).
    """
    if not teks:
        return teks

    # Daftar Kata Kotor
    BAD_WORDS = [
        # --- BAHASA INDONESIA & GAUL ---
        "anjing", "babi", "monyet", "kunyuk", "bajingan", "asu", "bangsat", "kampret",
        "kontol", "memek", "jembut", "ngentot", "ngewe", "perek", "pecun", "bencong",
        "banci", "mahode", "bego", "goblok", "idiot", "tolol", "sarap", "udik",
        "bodoh", "setan", "iblis", "tai", "berak", "geblek", "gila", "sinting",

        # --- BAHASA INGGRIS ---
        "fuck", "shit", "bitch", "asshole", "dick", "pussy", "cunt", "whore",
        "slut", "bastard", "motherfucker", "cock", "tits", "nigger", "fag",
        "sex", "porn", "nude", "horny", "sucks", "stupid", "moron",
        
        # --- BAHASA DAERAH (Jawa, Sunda, Batak, dll) ---
        "jancok", "cok", "jancuk", "gateli", "jamput", "jangkrik", # Jawa
        "matamu", "ndasmu", "cangkem", "kirik", 
        "goblog", "anying", "siamang", "kehed", "belegug", # Sunda
        "pantek", "puki", "kimak", "pukimak", "telaso", "bujang", # Sumatera/Sulawesi
        "bujanginam", "lonte",
    ]

    # Melakukan sensor
    for word in BAD_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        teks = pattern.sub("*" * len(word), teks)

    return teks


def verify_recaptcha(token):
    """
    Verifikasi token reCAPTCHA v3 ke server Google.
    Mengembalikan True jika sukses/skor aman, False jika gagal.
    """
    if not token:
        return False
        
    # --- BUG FIX: Bypass for Local Testing with Dummy Keys ---
    # reCAPTCHA v3 doesn't have test keys that return scores.
    # If using dummy keys in DEBUG mode, automatically pass.
    public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', '')
    if settings.DEBUG and public_key == '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI':
        return True

    url = 'https://www.google.com/recaptcha/api/siteverify'
    private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY', '')
    
    if not private_key:
        return False # Gagal jika key tidak disetting

    data = parse.urlencode({
        'secret': private_key,
        'response': token
    }).encode('utf-8')
    
    req = request.Request(url, data=data)
    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            # success & score >= 0.5 dihitung lolos v3
            return result.get('success', False) and result.get('score', 0.0) >= 0.5
    except Exception:
        return False