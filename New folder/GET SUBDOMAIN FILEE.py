
import os
import sublist3r

def get_subdomains(domain, all_subdomains_file, output_folder):
    try:
        # فتح الملفات في وضع الكتابة
        with open(all_subdomains_file, "a") as all_file, open(os.path.join(output_folder, f"{domain}_subdomains.txt"), "w") as domain_file:
            
            # استخراج السب دومينات باستخدام Sublist3r
            subdomains = sublist3r.main(domain, 40, None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)

            if subdomains:
                for subdomain in subdomains:
                    # الكتابة في ملف السب دومينات العام
                    all_file.write(subdomain + "\n")
                    
                    # الكتابة في الملف الخاص بالدومين الحالي
                    domain_file.write(subdomain + "\n")
    except Exception as e:
        print(f"An error occurred for {domain}: {str(e)}")

# الدالة الرئيسية لقراءة الدومينات من الملف ومعالجتها
def process_domains(file_name):
    try:
        # قراءة الدومينات من الملف
        with open(file_name, 'r') as file:
            domains = file.readlines()

        # إزالة المسافات البيضاء من كل سطر
        domains = [domain.strip() for domain in domains]

        # اسم الملف الذي سيحوي جميع السب دومينات
        all_subdomains_file = "all_subdomains.txt"
        
        # إنشاء مجلد جديد لتخزين ملفات السب دومينات المنفصلة
        output_folder = "subdomains_output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # استخراج السب دومينات لكل دومين وتخزينها
        for domain in domains:
            get_subdomains(domain, all_subdomains_file, output_folder)
        
        print(f"All subdomains have been saved in '{all_subdomains_file}' and individual files in the '{output_folder}' folder.")
    
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# الاستخدام
file_name = input("Enter the file name containing domains (e.g., domains.txt): ")
process_domains(file_name)
