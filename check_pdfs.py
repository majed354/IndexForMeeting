#!/usr/bin/env python3
"""
سكربت مساعد لأرشيف مجالس القسم
- يقرأ ملف CSV
- يولّد قائمة بأسماء ملفات PDF المطلوبة
- يتحقق من الملفات الموجودة والناقصة
"""

import csv
import os
from collections import defaultdict

def generate_pdf_name(year, month, council):
    """توليد اسم ملف PDF"""
    y = str(year)[-2:].zfill(2)
    m = str(month).zfill(2)
    c = str(council).zfill(2)
    return f"{y}{m}-{c}.pdf"

def main():
    csv_path = 'data/councils.csv'
    pdfs_dir = 'pdfs'
    
    if not os.path.exists(csv_path):
        print("❌ ملف CSV غير موجود!")
        return
    
    # قراءة CSV
    councils = defaultdict(set)
    total_topics = 0
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            year = row.get('السنة الهجرية', '').strip()
            month = row.get('الشهر الهجري', '').strip()
            council = row.get('رقم المجلس', '').strip()
            
            if year and month and council:
                pdf_name = generate_pdf_name(year, month, council)
                councils[(year, month, council)].add(pdf_name)
                total_topics += 1
    
    print("=" * 50)
    print("📊 إحصائيات الأرشيف")
    print("=" * 50)
    print(f"إجمالي الموضوعات: {total_topics}")
    print(f"عدد المجالس الفريدة: {len(councils)}")
    print()
    
    # توليد قائمة ملفات PDF
    pdf_files = set()
    for (year, month, council), pdfs in councils.items():
        pdf_files.update(pdfs)
    
    print("=" * 50)
    print("📄 ملفات PDF المطلوبة")
    print("=" * 50)
    
    # التحقق من الملفات الموجودة
    existing = set()
    if os.path.exists(pdfs_dir):
        existing = set(os.listdir(pdfs_dir))
    
    missing = pdf_files - existing
    found = pdf_files & existing
    
    print(f"✅ موجودة: {len(found)}")
    print(f"❌ ناقصة: {len(missing)}")
    print()
    
    if missing:
        print("=" * 50)
        print("📋 قائمة الملفات الناقصة")
        print("=" * 50)
        for pdf in sorted(missing):
            print(f"  {pdf}")
        print()
        
        # حفظ القائمة في ملف
        with open('missing_pdfs.txt', 'w', encoding='utf-8') as f:
            f.write("# ملفات PDF الناقصة\n")
            f.write("# ضعها في مجلد pdfs/\n\n")
            for pdf in sorted(missing):
                f.write(f"{pdf}\n")
        print("💾 تم حفظ القائمة في: missing_pdfs.txt")
    
    print()
    print("=" * 50)
    print("📁 قائمة جميع ملفات PDF المطلوبة")
    print("=" * 50)
    for pdf in sorted(pdf_files):
        status = "✅" if pdf in existing else "❌"
        print(f"  {status} {pdf}")

if __name__ == "__main__":
    main()
