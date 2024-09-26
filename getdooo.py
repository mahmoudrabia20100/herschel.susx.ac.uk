import sublist3r

def get_subdomains(domain):
    try:
        print(f"Finding subdomains for: {domain}")
        
        # استخراج السب دومينات مع استخدام المعاملات المطلوبة في الإصدار الحالي
        subdomains = sublist3r.main(domain, 40, f"{domain}_subdomains.txt", ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
        
        if subdomains:
            print(f"Found {len(subdomains)} subdomains:")
            
            # حفظ السب دومينات في ملف نصي
            filename = f"{domain}_subdomains.txt"
            with open(filename, "w") as file:
                for subdomain in subdomains:
                    print(subdomain)  # الطباعة في الكونسول
                    file.write(subdomain + "\n")  # حفظ السب دومينات في الملف النصي
            print(f"Subdomains have been saved to {filename}")
        else:
            print("No subdomains found.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
domain = input("Enter the domain (e.g., example.com): ")
get_subdomains(domain)
