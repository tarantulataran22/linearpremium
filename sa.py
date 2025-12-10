import os
import json

# Aranacak offset isimleri
offset_names = [
    "dwLocalPlayerPawn",
    "dwEntityList",
    "dwViewMatrix",
    "dwGameRules",
    "dwViewAngles",
    "ForceJumpAddress"
]

def find_offsets(obj, offsets_found):
    """JSON objesini recursive tara, offsetleri bul"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in offset_names and offsets_found[k] == -1:
                offsets_found[k] = v
            find_offsets(v, offsets_found)
    elif isinstance(obj, list):
        for item in obj:
            find_offsets(item, offsets_found)

# Çalıştırıldığı klasördeki tüm json dosyalarını tara
for filename in os.listdir("."):
    if filename.lower().endswith(".json"):
        offsets_found = {name: -1 for name in offset_names}
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            find_offsets(data, offsets_found)
            
            print(f"\n{filename} için offsetler:")
            for name, value in offsets_found.items():
                if value != -1:
                    print(f"static long {name}Offset = 0x{value:X};")
                else:
                    print(f"static long {name}Offset = -1;  // Değer bulunamadı")
        except Exception as e:
            print(f"{filename} dosyası okunamadı: {e}")
