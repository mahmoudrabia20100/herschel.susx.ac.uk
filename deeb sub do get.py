import sublist3r

def get_subdomains(domain):
    try:
        print(f"Finding subdomains for: {domain}")

        # فتح الملف في وضع الكتابة
        filename = f"{domain}_subdomains.txt"
        with open(filename, "w") as file:
            # Perform deep subdomain search
            subdomains = sublist3r.main(
                domain, 
                40, 
                None,  # لا حاجة لتحديد ملف إخراج هنا
                ports=None, 
                silent=True, 
                verbose=False,  # تعيين إلى False لمنع الطباعة التفصيلية
                enable_bruteforce=True,  # تمكين brute force لعملية بحث أعمق
                engines=None  # استخدام جميع المحركات المتاحة
            )

            # الكتابة في الملف فورًا بعد العثور على كل سب دومين
            if subdomains:
                for subdomain in subdomains:
                    file.write(subdomain + "\n")
                print(f"Subdomains have been saved to {filename}")
            else:
                print("No subdomains found.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# مثال على الاستخدام
domain = input("Enter the domain (e.g., example.com): ")
get_subdomains(domain)
