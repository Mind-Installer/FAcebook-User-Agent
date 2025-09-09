import os
import random
import requests
import tkinter as tk
from tkinter import messagebox
import re

# =====================================
# Helpers / Banner
# =====================================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    banner = r"""
                       ██████╗ ██████╗ ███╗   ██╗██╗   ██╗██╗██╗  ██╗                       
                      ██╔════╝██╔═══██╗████╗  ██║██║   ██║██║╚██╗██╔╝                       
                      ██║     ██║   ██║██╔██╗ ██║██║   ██║██║ ╚███╔╝                        
                      ██║     ██║   ██║██║╚██╗██║██║   ██║██║ ██╔██╗                        
                      ╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║██╔╝ ██╗                       
                       ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═╝                       
    """
    print("=" * 100)
    print(banner)
    print("=" * 100)
    print("F A C E B O O K   U S E R   A G E N T   G E N E R A T O R".center(100))
    print("=" * 100)

# =====================================
# Locale / Carrier detection
# =====================================
def sanitize_fbcr(carrier: str) -> str:
    if not carrier:
        return "Carrier"
    return re.sub(r"[^A-Za-z0-9]", "", carrier)

def get_locale_and_carrier(ip):
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        country = resp.get("country", "Unknown")
        country_code = resp.get("countryCode", "US")
        isp = resp.get("isp", "Carrier")
    except Exception:
        country = "Unknown"
        country_code = "US"
        isp = "Carrier"

    locale_map = {
        "US": "en_US", "GB": "en_GB", "CA": "en_CA", "AU": "en_AU",
        "IN": "en_IN", "SG": "en_SG", "PH": "en_PH",
        "FR": "fr_FR", "BE": "fr_BE", "CH": "fr_CH",
        "DE": "de_DE", "AT": "de_AT",
        "ES": "es_ES", "MX": "es_MX", "AR": "es_AR", "CO": "es_CO",
        "CL": "es_CL", "PE": "es_PE",
        "PT": "pt_PT", "BR": "pt_BR",
        "IT": "it_IT", "NL": "nl_NL", "RU": "ru_RU", "UA": "uk_UA",
        "BG": "bg_BG", "RS": "sr_RS",
        "CN": "zh_CN", "TW": "zh_TW", "HK": "zh_HK",
        "JP": "ja_JP", "KR": "ko_KR",
        "TR": "tr_TR", "SA": "ar_SA", "EG": "ar_EG",
        "IR": "fa_IR", "IL": "he_IL"
    }

    locale = locale_map.get(country_code, "en_US")
    fbcr = sanitize_fbcr(isp)
    return country, country_code, locale, fbcr

# =====================================
# iOS mappings (XS -> 16 Pro Max, no mini)
# =====================================
iphone_models_fbss = {
    "iPhone11,2": 3, "iPhone11,4": 3, "iPhone11,6": 3, "iPhone11,8": 2,
    "iPhone12,1": 2, "iPhone12,3": 3, "iPhone12,5": 3,
    "iPhone13,2": 3, "iPhone13,3": 3, "iPhone13,4": 3,
    "iPhone14,5": 3, "iPhone14,2": 3, "iPhone14,3": 3,
    "iPhone14,7": 3, "iPhone15,2": 3, "iPhone15,3": 3,
    "iPhone15,4": 3, "iPhone15,5": 3, "iPhone16,1": 3, "iPhone16,2": 3,
    "iPhone17,1": 3, "iPhone17,2": 3, "iPhone17,3": 3, "iPhone17,4": 3,
}

ios_builds_map = {
    "18.0": ["22A3354", "22A3351", "22A3370"],
    "18.1": ["22B83", "22B91"],
    "18.2": ["22C152"],
    "18.2.1": ["22C161"],
    "18.3": ["22D63", "22D60"],
    "18.3.1": ["22D72"],
    "18.3.2": ["22D82"],
    "18.4": ["22E240"],
    "18.4.1": ["22E252"],
    "18.5": ["22F76"],
    "18.6": ["22G86"],
    "18.6.2": ["22G100"],
}

fb_ios_triplets = [
    ("526.0.0.61.97", "776821927", "776821927"),
    ("525.0.0.53.107", "774177433", "774177433"),
    ("524.0.0.49.109", "772009221", "772009221"),
    ("523.0.0.42.94", "770111003", "770111003"),
]

ua_template_ios = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Mobile/{build} "
    "[FBAN/FBIOS;FBAV/{fbav};FBBV/{fbbv};"
    "FBDV/{device};FBMD/iPhone;FBSN/iOS;FBSV/{ios_ver};"
    "FBSS/{fbss};FBID/phone;FBLC/{locale};FBCR/{fbcr};FBOP/5;"
    "FBRV/{fbrv};IABMV/{iabmv}]"
)

# =====================================
# Full Android Devices (70+ US Premium)
# =====================================
android_devices = [
    # Samsung Galaxy S24 Series
    {"brand":"samsung","model":"SM-S928U","android_ver":"14","build":"UP1A.240105.002","density":3.5,"width":1440,"height":3088},
    {"brand":"samsung","model":"SM-S926U","android_ver":"14","build":"UP1A.240105.002","density":3.4,"width":1440,"height":3120},
    {"brand":"samsung","model":"SM-S921U","android_ver":"14","build":"UP1A.240105.002","density":3.0,"width":1080,"height":2340},
    # Samsung Galaxy S23 Series
    {"brand":"samsung","model":"SM-S918U","android_ver":"13","build":"TP1A.220905.001","density":3.5,"width":1440,"height":3088},
    {"brand":"samsung","model":"SM-S916U","android_ver":"13","build":"TP1A.220905.001","density":3.4,"width":1440,"height":3120},
    {"brand":"samsung","model":"SM-S911U","android_ver":"13","build":"TP1A.220905.001","density":3.0,"width":1080,"height":2340},
    # Samsung Fold/Flip
    {"brand":"samsung","model":"SM-F946U","android_ver":"14","build":"UP1A.240105.002","density":3.2,"width":1812,"height":2176},
    {"brand":"samsung","model":"SM-F731U","android_ver":"14","build":"UP1A.240105.002","density":3.1,"width":1080,"height":2640},
    {"brand":"samsung","model":"SM-F936U","android_ver":"13","build":"TP1A.220905.001","density":3.1,"width":1812,"height":2176},
    {"brand":"samsung","model":"SM-F721U","android_ver":"13","build":"TP1A.220905.001","density":3.0,"width":1080,"height":2640},
    # Samsung Older
    {"brand":"samsung","model":"SM-N986U","android_ver":"12","build":"SP1A.210812.016","density":3.5,"width":1440,"height":3088},
    {"brand":"samsung","model":"SM-S908U","android_ver":"13","build":"TP1A.220905.001","density":3.5,"width":1440,"height":3088},

    # Google Pixel 8/7/6/5
    {"brand":"Pixel","model":"Pixel 8 Pro","android_ver":"14","build":"AP2A.240405.002","density":3.5,"width":1344,"height":2992},
    {"brand":"Pixel","model":"Pixel 8","android_ver":"14","build":"AP2A.240405.002","density":3.2,"width":1080,"height":2400},
    {"brand":"Pixel","model":"Pixel 7 Pro","android_ver":"13","build":"TQ3A.230901.001","density":3.3,"width":1440,"height":3120},
    {"brand":"Pixel","model":"Pixel 7","android_ver":"13","build":"TQ3A.230901.001","density":3.0,"width":1080,"height":2400},
    {"brand":"Pixel","model":"Pixel 6 Pro","android_ver":"12","build":"SQ3A.220705.003.A1","density":3.3,"width":1440,"height":3120},
    {"brand":"Pixel","model":"Pixel 6","android_ver":"12","build":"SQ3A.220705.003.A1","density":3.0,"width":1080,"height":2400},
    {"brand":"Pixel","model":"Pixel 5","android_ver":"11","build":"RQ3A.210905.001","density":3.0,"width":1080,"height":2340},

    # OnePlus
    {"brand":"OnePlus","model":"CPH2573","android_ver":"14","build":"PHB110_14.0.0","density":3.3,"width":1440,"height":3168},
    {"brand":"OnePlus","model":"CPH2449","android_ver":"13","build":"NE2215_13.1.0","density":3.0,"width":1260,"height":2800},
    {"brand":"OnePlus","model":"LE2125","android_ver":"12","build":"SKQ1.210216.001","density":3.3,"width":1440,"height":3216},

    # Motorola
    {"brand":"motorola","model":"XT2301-4","android_ver":"14","build":"T1TR33.62-15-5","density":3.0,"width":1080,"height":2400},
    {"brand":"motorola","model":"XT2323-3","android_ver":"14","build":"T1TRS33.10-5-15","density":3.1,"width":1080,"height":2640},

    # Asus
    {"brand":"ASUS","model":"ASUS_AI2205","android_ver":"13","build":"WW_33.0820.0810.121","density":3.2,"width":1080,"height":2448},
    {"brand":"ASUS","model":"ASUS_AI2302","android_ver":"14","build":"WW_34.1010.0101.241","density":3.3,"width":1080,"height":2400},

    # Nothing
    {"brand":"Nothing","model":"A065","android_ver":"14","build":"NothingOS1.5.4","density":3.1,"width":1080,"height":2412},
    {"brand":"Nothing","model":"A063","android_ver":"13","build":"NothingOS1.1.8","density":3.1,"width":1080,"height":2400},

    # Sony Xperia
    {"brand":"SONY","model":"XQ-DQ72","android_ver":"14","build":"67.1.A.2.86","density":3.2,"width":1644,"height":3840},
    {"brand":"SONY","model":"XQ-CT72","android_ver":"13","build":"61.1.A.2.211","density":3.0,"width":1080,"height":2520},

    # Xiaomi
    {"brand":"Xiaomi","model":"2304FPN6DG","android_ver":"14","build":"UP1A.230905.007","density":3.4,"width":1440,"height":3200},
    {"brand":"Xiaomi","model":"2201122G","android_ver":"13","build":"TKQ1.211230.002","density":3.2,"width":1440,"height":3200},

    # Vivo
    {"brand":"vivo","model":"V2309","android_ver":"14","build":"UP1A.230905.007","density":3.5,"width":1440,"height":3200},
    {"brand":"vivo","model":"V2241A","android_ver":"13","build":"TKQ1.221114.001","density":3.2,"width":1440,"height":3200},
]

# =====================================
# Latest 5 Facebook Android versions
# =====================================
fb_triplets_android = [
    ("529.0.0.44.73", "BUILD_52944"),
    ("528.0.0.62.74", "BUILD_52862"),
    ("527.0.0.59.76", "BUILD_52759"),
    ("526.1.0.66.75", "BUILD_52666"),
    ("525.0.0.53.51", "BUILD_52553"),
]

ua_template_android = (
    "Mozilla/5.0 (Linux; Android {android_ver}; {model} Build/{build}; wv) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
    "Chrome/{chrome_ver} Mobile Safari/537.36 "
    "[FBAN/FB4A;FBAV/{fbav};FBBV/{fbbv};FBPN/com.facebook.katana;"
    "FBLC/{locale};FBBR/{brand};FBCR/{fbcr};FBMF/{brand};"
    "FBDV/{model};FBSV/{android_ver};FBCA/arm64-v8a:;"
    "FBDM{{density={density},width={width},height={height}}};FB_FW/1;FBOP/6]"
)

# =====================================
# Generators
# =====================================
def generate_ios_user_agents(locale, fbcr, count=10):
    ua_list = []
    for _ in range(count):
        ios_ver, builds = random.choice(list(ios_builds_map.items()))
        build = random.choice(builds)
        device, fbss = random.choice(list(iphone_models_fbss.items()))
        fbav, fbbv, fbrv = random.choice(fb_ios_triplets)
        iabmv = random.choice(["1", "3"])
        ua = ua_template_ios.format(
            ios_ver=ios_ver.replace(".", "_"),
            build=build,
            fbav=fbav,
            fbbv=fbbv,
            device=device,
            fbss=fbss,
            locale=locale,
            fbcr=fbcr,
            fbrv=fbrv,
            iabmv=iabmv,
        )
        ua_list.append((ua, {"brand":"Apple","model":device}))
    return ua_list

def generate_android_user_agents(locale, fbcr, count=10):
    ua_list = []
    chrome_pool = ["124.0.6367.54", "123.0.6312.80", "122.0.6261.105"]
    for _ in range(count):
        dev = random.choice(android_devices)
        fbav, fbbv = random.choice(fb_triplets_android)
        chrome_ver = random.choice(chrome_pool)
        ua = ua_template_android.format(
            android_ver=dev["android_ver"],
            model=dev["model"],
            build=dev["build"],
            chrome_ver=chrome_ver,
            fbav=fbav,
            fbbv=fbbv,
            brand=dev["brand"],
            locale=locale,
            fbcr=fbcr,
            density=dev["density"],
            width=dev["width"],
            height=dev["height"]
        )
        ua_list.append((ua, dev))
    return ua_list

# =====================================
# Popup UI with per-UA copy
# =====================================
def show_popup(user_agents, header_text, country, locale, fbcr, on_close_callback):
    root = tk.Tk()
    root.title("CONVIX — Facebook UA Generator")
    root.geometry("1200x700")
    root.configure(bg="#0f1220")

    header = tk.Frame(root, bg="#0b0e1a")
    header.pack(fill="x")
    tk.Label(header, text=header_text, fg="#00ffae", bg="#0b0e1a",
             font=("Consolas", 16, "bold")).pack(pady=10)

    info = tk.Label(root,
                    text=f"🌍 {country} | 🌐 {locale} | 📶 {fbcr}",
                    fg="#ccc", bg="#0f1220", font=("Consolas", 12))
    info.pack(pady=5)

    canvas = tk.Canvas(root, bg="#0f1220", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#0f1220")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for ua, dev in user_agents:
        frame = tk.Frame(scroll_frame, bg="#1a1f35", bd=1, relief="solid")
        frame.pack(fill="x", padx=8, pady=6)

        tk.Label(frame, text=f"[{dev['brand']} {dev['model']}]", 
                 fg="#00ffae", bg="#1a1f35", font=("Consolas", 11, "bold")).pack(anchor="w", padx=8, pady=3)

        ua_label = tk.Text(frame, wrap="word", height=3, font=("Consolas", 9),
                          bg="#0f1220", fg="#e6e6e6", insertbackground="white")
        ua_label.insert("1.0", ua)
        ua_label.config(state="disabled")
        ua_label.pack(fill="x", padx=8, pady=3)

        def make_copy_button(text=ua):
            return lambda: (root.clipboard_clear(), root.clipboard_append(text),
                            messagebox.showinfo("Copied", "UA copied to clipboard!"))

        tk.Button(frame, text="📋 Copy", command=make_copy_button(),
                  bg="#00ffae", fg="black", font=("Consolas", 10, "bold")).pack(anchor="e", padx=8, pady=4)

    def on_close():
        root.destroy()
        on_close_callback()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

# =====================================
# Main Loop
# =====================================
def main_loop():
    print_banner()
    while True:
        print("Choose User Agent Category:")
        print("1) Facebook iOS")
        print("2) Facebook Android")
        choice = input("Enter choice (1 or 2): ").strip()

        ip = input("Enter IP address (or press Enter for auto-detect): ").strip()
        if not ip:
            ip = ""

        country, country_code, locale, fbcr = get_locale_and_carrier(ip)

        def restart_menu():
            main_loop()

        if choice == "1":
            uas = generate_ios_user_agents(locale, fbcr, count=20)
            show_popup(uas, "📱 Facebook iOS User Agents", country, locale, fbcr, restart_menu)
            break
        elif choice == "2":
            uas = generate_android_user_agents(locale, fbcr, count=20)
            show_popup(uas, "🤖 Facebook Android User Agents", country, locale, fbcr, restart_menu)
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main_loop()
