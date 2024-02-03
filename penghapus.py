import pandas as pd
import sys
from termcolor import colored as cl
import re
import os
import subprocess
import time
import numpy as np

un = 'Unnamed'
en = 'latin1'
xl = 'xlrd'
px = 'openpyxl'
ut = 'utf-8'
# karakterAneh = ['sksksks', '\u00C2', '????????', 'Ã£Â‚Ã¢Â²', 'ÃƒÂ‚Ã‚Â²', 'ÃƒÂ‚Ã‚Â”', 'Â‘yeeekÂ’'] #isi disini yang ingin dihapus
# karakterAman = r'[^a-zA-Z0-9\s,.!#@?/:*-]' #isi disini yang ingin diamankan
# singleNonVocal = r'(?<![aeiouAEIOU])[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ](?![aeiouAEIOU])' #cek huruf single non vocal
# karakterJamak = r'(\S)(\1{2,})'
col = "full_text"
sel = "selesai"
prs = "Proses hapus"
uu = "Proses selesai, silahkan cek file"
ff = ["mention", "tagar", "url"]
dir = os.getcwd()
sementara = []

def logo():
    print(cl("  ___\n /__/\n/enghapus (by CukiD)","magenta"))

def ma():
    print(cl("Mode Auto","green"))

if len(sys.argv) <= 1:
    logo()
    print("\nUntuk bantuan:\n python penghapus.py [-h/--help]\n")
elif len(sys.argv) == 2 and (str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help"):
    logo()
    print("""\nMenu:\n  [-m/mention]  - hapus @/mention
  [-u/url]      - hapus url
  [-t/tagar]    - hapus tagar
  [-k/konversi] - konversi format tabel
  [-x/xls]      - konversi excel(xls/xlsx) ke csv
  [-u/unnamed]  - menghapus semua tabel yang berisikan nilai unnamed
  [-l/lower]    - merubah semua font menjadi lower
  [-a/auto]     - deteksi format dan auto konversi, hapus (mention, url, tagar)

Untuk penggunaan:
  python penghapus.py [-m/mention] [targetFile.csv] [outputFile.csv]
  python penghapus.py [-u/url] [targetFile.csv] [outputFile.csv]
  python penghapus.py [-t/tagar] [targetFile.csv] [outputFile.csv]
  python penghapus.py [-k/konversi] [targetFile.csv] [outputFile.csv]
  python penghapus.py [-x/xls] [targetFile.xls/.xlsx] [outputFile.csv]
  python penghapus.py [-un/unnamed] [targetFile.csv] [outputFile.csv]
  python penghapus.py [-l/lower] [targetFile.csv] [outputFile.csv]
  python penghapus.py [-a/auto] [targetFile.xls/.xlsx/.csv] [outputFile.csv]\n""")
#[-f/filter]   - menghapus karakter non ascii , karakter jamak, huruf non vocal single (belum done)
#[-i/invalid]  - memperbaiki yang statusnya invalid (belum done)
#python penghapus.py [-f/filter] [targetFile.csv] [outputFile.csv]
#python penghapus.py [-i/invalid] [targetFile.csv] [outputFile.csv]

elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-k" or str(sys.argv[1]) == "konversi") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
    logo()
    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses konversi format tabel pada {file}")
    data = pd.read_csv(file, sep=';')
    data.to_csv(output, index=False)
    print(cl(f"Proses selesai, silahkan cek file {output}\n","green"))
# elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-f" or str(sys.argv[1]) == "filter") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
#     file = str(sys.argv[2])
#     output = str(sys.argv[3])
#     def bersih2(text):
#         if isinstance(text, str):
#             filter1 = re.sub(karakterAman, '', str(text))
#             filter2 = re.sub(singleNonVocal, '', str(filter1))
#             filter3 = re.sub(karakterJamak, r'\1', str(filter2))
#             for key in karakterAneh:
#                 filter3.replace(str(key), '')
#             return  filter3
#         else:
#             print(cl("Format bukan string","yellow"))
#             sys.exit()
    
#     print(f"\nProses hapus karakter non ascii, karakter jamak, huruf non vocal single pada {file}")
#     data = pd.read_csv(file, encoding=en)
#     data[col].apply(bersih2)
#     data.to_csv(output, index=False)
#     print(cl(f"Proses selesai, silahkan cek file {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-x" or str(sys.argv[1]) == "xls") and ('.xls' in str(sys.argv[2]) or '.xlsx' in str(sys.argv[2])) and '.csv' in str(sys.argv[3]):
    logo()
    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses konversi format pada {file} ke format csv")
    data = pd.read_excel(file)
    data.to_csv(output, index=False)
    print(cl(f"{uu} {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-l" or str(sys.argv[1]) == "lower") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
    logo()
    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses konversi all value pada {file} ke lower")
    data = pd.read_csv(file, encoding=en)
    data = data.astype(str).apply(lambda x: x.str.lower())
    data.to_csv(output, index=False)
    print(cl(f"{uu} {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-un" or str(sys.argv[1]) == "unnamed") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
    logo()
    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses hapus tabel bervalue unnamed pada {file}")
    data = pd.read_csv(file, encoding=en)
    fixdata = data[data.filter(regex='^(?!Unnamed)').columns]
    if fixdata.empty:
        print(cl(f"Unnamed tidak ditemukan pada {file}\n", "yellow"))
    else:
        fixdata.to_csv(output, index=False)
        print(cl(f"{uu} {output}\n","green"))        
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-m" or str(sys.argv[1]) == "mention") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
    logo()
    def hapusMention(text):
        if isinstance(text, str):
            nggoleki = re.sub(r'@\S+', '', text)
            return nggoleki
        else:
            print(cl("Format bukan string","yellow"))
            sys.exit()

    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses hapus mention pada {file}")
    data = pd.read_csv(file, encoding=en)
    data[col] = data[col].apply(hapusMention)
    data.to_csv(output, index=False)
    print(cl(f"{uu} {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-u" or str(sys.argv[1]) == "url") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
    logo()
    def hapusUrl(text):
        if isinstance(text, str):
            nggoleki = re.sub(r'https\S+', '', text)
            return nggoleki
        else:
            print(cl("Format bukan string","yellow"))
            sys.exit()

    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses hapus url pada {file}")
    data = pd.read_csv(file, encoding=en)
    data[col] = data[col].apply(hapusUrl)
    data.to_csv(output, index=False)
    print(cl(f"{uu} {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-s" or str(sys.argv[1]) == "spasi") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):    
    logo()
    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses hapus spasi pada {file}")
    data = pd.read_csv(file, encoding=en)
    data[col] = data[col].apply(lambda x: x.lstrip())
    data.to_csv(output, index=False)
    print(cl(f"{uu} {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-t" or str(sys.argv[1]) == "tagar") and '.csv' in str(sys.argv[2]) and '.csv' in str(sys.argv[3]):
    logo()
    def hapusTagar(text):
        if isinstance(text, str):
            nggoleki = re.sub(r'#\S+', '', text)
            return nggoleki
        else:
            print(cl("Format bukan string","yellow"))
            return nggoleki

    file = str(sys.argv[2])
    output = str(sys.argv[3])
    print(f"\nProses hapus spasi pada {file}")
    data = pd.read_csv(file, encoding=en)
    data[col] = data[col].apply(hapusTagar)
    data.to_csv(output, index=False)
    print(cl(f"{uu} {output}\n","green"))
elif len(sys.argv) > 3 and len(sys.argv) < 5 and (str(sys.argv[1]) == "-a" or str(sys.argv[1]) == "auto") and ('.csv' in str(sys.argv[2]) or '.xls' in str(sys.argv[2]) or '.xlsx' in str(sys.argv[2])) and '.csv' in str(sys.argv[3]):

    def perintah(cmd):
        try:
            subprocess.run(cmd, shell=True, cwd=dir, check=True)
        except subprocess.CalledProcessError as e:
            print(cl(f"Terdapat kesalahan {e}\n","yellow"))

    def mention(text):
        if isinstance(text, str):
            nggoleki = re.sub(r'@\S+', '', text)
            return nggoleki
        else:
            nggoleki = re.sub(r'@\S+', '', str(text))
            print(cl("Format bukan string","yellow"))
            return nggoleki

    def tagar(text):
        if isinstance(text, str):
            nggoleki = re.sub(r'#\S+', '', text)
            return nggoleki
        else:
            print(cl("Format bukan string","yellow"))
            sys.exit()

    def url(text):
        if isinstance(text, str):
            nggoleki = re.sub(r'https\S+', '', text)
            return nggoleki
        else:
            print(cl("Format bukan string","yellow"))
            sys.exit()
    def unammed(text, tt, fl, pp):
        yuhu = text[text.filter(regex='^(?!Unnamed)').columns]
        if yuhu.empty:
            print(cl(f"Unnamed tidak ditemukan pada {fl}", "yellow"))
            return yuhu
        else:
            print(cl(f"{tt} unnamed pada {fl} {pp}","green"))
            return yuhu

    def open(fl, ii, out, dlt, copy, ren, ss):
        if fl.endswith(('.xls', '.xlsx')):
            n = str(fl).split('.')
            jj = out.split('.')
            ee = f"{jj[0]}2.csv"
            aa = ren
            print(cl(f"\nFormat file {n[1]}","green"))
            fl = pd.read_excel(fl)
            fl = unammed(fl, ii, ee, ss)
            print(cl(f"File {n[0]}.{n[1]} disimpan ke format csv","green"))
            fl.to_csv(out, index=False)
            time.sleep(1)
            print(cl(f"File {n[0]}.{n[1]} disimpan ke format csv {ss}","green"))
            print(cl(f"Clone file {out} ke {ee}","green"))
            perintah(copy)
            print(cl(f"Clone file {out} ke {ee} {ss}","green"))
            print(cl(f"Hapus file {out}","green"))
            perintah(dlt)
            print(cl(f"Hapus file {out} {ss}","green"))
            print(cl(f"Membaca file {ee}","green"))
            fl = pd.read_csv(ee, sep=';')
            hai = fl['created_at'].sum()
            kk = fl.head(0)d
            for uhui in kk:
                if uhui == "created_at":
                    vv = fl[uhui]
                    for nn in vv:
                        ok = nn.split(';')
                        sementara.append(kk)
                        sementara.append(ok)
                    
                    
                        
            # i = 0
            # for uu in kk:
            #     if uu == "created_at":
            #         for _ in range(totbaris):
            #             print(fl.iloc[0])
            # fl[bb] = fl[kk[0]].str.split(';', expand=True)
            # i = 0
            # for _ in range(10):
            #     fl[kk[i]] = fl[kk[i]].str.strip('"')
            #     i += 1
            print(cl(f"Membaca file {ee} {ss}","green"))
            print(cl(f"Proses menyimpan file {ee}","green"))
            # fl.to_csv(ee, index=False)
            # time.sleep(1)
            # print(cl(f"Proses menyimpan file {ee} {ss}","green"))
            # print(cl(f"Rubah file {ee} ke {out}","green"))
            # perintah(mv)
            # print(cl(f"Rubah file {ee} ke {out} {ss}","green"))
            # print(cl(f"Membaca file {ee}","green"))
            # fl = pd.read_csv(out, encoding='latin1')
            # print(cl(f"{ii} unnamed pada {ee}","green"))
            # fl = unammed(fl, ii, ee, ss)
            sys.exit()
            return fl
        elif fl.endswith('.csv'):
            print(cl(f"\nFormat file sudah csv","green"))
            print(cl(f"Membaca file {fl}","green"))
            fl = pd.read_csv(fl, sep=';')
            print(cl(f"Membaca file {fl} {ss}","green"))
            return fl

    try:
        logo()
        ma()
        file = str(sys.argv[2])
        output = str(sys.argv[3])
        d = f"del {output}"
        nf = output.split('.')
        cp = f"copy {output} {nf[0]}2.csv"
        mv = f"move {nf[0]}2.csv {output}"
        data = open(file, prs, output, d, cp, mv, sel)
        if file.endswith('.csv'):
            print(cl(f"{prs} {ff[0]} pada {file}","green"))
            data[col] = data[col].astype(str).apply(mention)
            print(cl(f"{prs} {ff[0]} pada {file} {sel}","green"))
            print(cl(f"{prs} {ff[1]} pada {file}","green"))
            data[col] = data[col].astype(str).apply(tagar)
            print(cl(f"{prs} {ff[1]} pada {file} {sel}","green"))
            print(cl(f"{prs} {ff[2]} pada {file}","green"))
            data[col] = data[col].astype(str).apply(url)
            print(cl(f"{prs} {ff[2]} pada {file} {sel}","green"))
            print(cl(f"{prs} unnamed pada {file}","green"))
            data = unammed(data, prs, output, file, sel)
            print(cl(f"{prs} unnamed pada {file} {sel}","green"))
            print(cl(f"{prs} spasi depan berlebih pada {file}","green"))
            data[col] = data[col].astype(str).apply(lambda x: x.lstrip())
            print(cl(f"{prs} spasi depan berlebih pada {file} {sel}","green"))
            print(cl(f"Proses konversi all value pada {file} ke lower","green"))
            data = data.astype(str).apply(lambda x: x.str.lower())
            print(cl(f"Proses konversi all value pada {file} ke lower {sel}","green"))
            print(cl(f"Proses menyimpan file {output}","green"))
            data.to_csv(output, index=False)
            print(cl(f"Proses menyimpan file {output} {sel}","green"))
            print(cl(f"{uu} {output}\n","green"))
        else:
            out = output.split('.')
            file2 = f"{out[0]}2.csv"
            print(cl(f"{prs} {ff[0]} pada {file2}","green"))
            data[col] = data[col].astype(str).apply(mention)
            print(cl(f"{prs} {ff[0]} pada {file2} {sel}","green"))
            print(cl(f"{prs} {ff[1]} pada {file2}","green"))
            data[col] = data[col].astype(str).apply(tagar)
            print(cl(f"{prs} {ff[1]} pada {file2} {sel}","green"))
            print(cl(f"{prs} {ff[2]} pada {file2}","green"))
            data[col] = data[col].astype(str).apply(url)
            print(cl(f"{prs} {ff[2]} pada {file2} {sel}","green"))
            print(cl(f"{prs} spasi depan berlebih pada {file2}","green"))
            data[col] = data[col].astype(str).apply(lambda x: x.lstrip())
            print(cl(f"{prs} spasi depan berlebih pada {file2} {sel}","green"))
            print(cl(f"Proses konversi all value pada {file2} ke lower","green"))
            data = data.astype(str).apply(lambda x: x.str.lower())
            print(cl(f"Proses konversi all value pada {file2} ke lower {sel}","green"))
            print(cl(f"Proses menyimpan data ke {file2}","green"))
            data.to_csv(file2, index=False)
            time.sleep(1)   
            print(cl(f"Proses menyimpan data ke {file2} {sel}","green"))
            print(cl(f"Rubah file {file2} ke {output}","green"))
            perintah(mv)
            print(cl(f"Rubah file {file2} ke {output} {sel}","green"))
            print(cl(f"{uu} {output}\n","green"))
    except KeyboardInterrupt:
        print(cl("Program diclose ya","red"))
        sys.exit()
else:
    logo()
    print(cl("\nUntuk bantuan:\n python penghapus.py [-h/--help]\n","yellow"))