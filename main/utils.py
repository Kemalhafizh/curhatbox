import re

def sensor_kata(teks):
    """
    Mengganti kata-kata kasar dengan tanda bintang (*).
    Mendukung Case Insensitive (Huruf besar/kecil tetap kena).
    """
    
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