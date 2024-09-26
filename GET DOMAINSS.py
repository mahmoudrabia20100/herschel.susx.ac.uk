import csv

# اسم الملف الذي يحتوي على قائمة الدومينات (تأكد من تطابق الاسم مع اسم الملف لديك)
file_name = 'tranco_Z3J4G.csv'

try:
    # فتح الملف وقراءة محتوياته
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # تخطي عنوان الأعمدة إذا كان موجودًا في الملف
        next(reader)

        # تصفية الدومينات للاحتفاظ فقط بتلك التي تحتوي على النطاق .uk
        uk_domains = [row[1] for row in reader if row[1].endswith('.uk')]

    # حفظ الدومينات .uk في ملف نصي
    with open('uk_domains.txt', 'w') as file:
        for domain in uk_domains:
            file.write(domain + '\n')

    print('تم استخراج وحفظ الدومينات ذات النطاق .uk في ملف uk_domains.txt.')

except FileNotFoundError:
    print(f"خطأ: لم يتم العثور على الملف '{file_name}'.")
except Exception as e:
    print(f"حدث خطأ أثناء قراءة الملف: {e}")
