import requests
import dns.resolver
import ssl
import socket
import json
import os

# قائمة من التوقيعات المرتبطة بالخدمات المختلفة للاستحواذ
TAKEOVER_SIGNATURES = {
    "GitHub Pages": "there isn't a github pages site here",
    "Amazon S3": "the specified bucket does not exist",
    "Heroku": "no such app",
    "Shopify": "sorry, this shop is currently unavailable",
    "Cloudfront": "bad request: could not resolve host",
    "Bitbucket": "repository not found",
    "Squarespace": "this domain is not properly configured",
    "Wix": "looks like this domain isn't connected to a website yet",
    "Tumblr": "there's nothing here.",
    "Fastly": "unknown domain",
    "Zendesk": "help center closed",
    "WordPress": "the site you were looking for, is no longer available"
}

def resolve_dns(subdomain):
    dns_info = {
        "A_records": [],
        "CNAME_records": [],
        "MX_records": []
    }
    try:
        print(f"Resolving A records for {subdomain}...")
        a_records = dns.resolver.resolve(subdomain, 'A')
        dns_info["A_records"] = [str(ip) for ip in a_records]
    except Exception as e:
        print(f"Failed to resolve A records for {subdomain}: {e}")
    
    try:
        print(f"Resolving CNAME records for {subdomain}...")
        cname_records = dns.resolver.resolve(subdomain, 'CNAME')
        dns_info["CNAME_records"] = [str(cname.target) for cname in cname_records]
    except Exception as e:
        print(f"Failed to resolve CNAME records for {subdomain}: {e}")
    
    try:
        print(f"Resolving MX records for {subdomain}...")
        mx_records = dns.resolver.resolve(subdomain, 'MX')
        dns_info["MX_records"] = [str(mx.exchange) for mx in mx_records]
    except Exception as e:
        print(f"Failed to resolve MX records for {subdomain}: {e}")

    return dns_info

def check_ssl(subdomain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((subdomain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=subdomain) as ssock:
                cert = ssock.getpeercert()
                print(f"SSL certificate for {subdomain}: {cert}")
                return cert
    except Exception as e:
        print(f"Failed to get SSL certificate for {subdomain}: {e}")
        return None

def check_takeover(subdomain, output_file):
    is_vulnerable = False

    for protocol in ['https', 'http']:
        try:
            url = f"{protocol}://{subdomain}"
            response = requests.get(url, timeout=10)
            response_text = response.text.lower()

            # البحث عن إشارات الاستحواذ
            for service, signature in TAKEOVER_SIGNATURES.items():
                if signature in response_text:
                    print(f"[!] Vulnerable to takeover on {service}: {subdomain}")
                    output_file.write(f"{subdomain}, Service: {service}, URL: {url}\n")
                    is_vulnerable = True
                    break

            # إذا كان الاستجابة هي 404
            if response.status_code == 404:
                print(f"[!] Potentially vulnerable (404): {subdomain}")
                output_file.write(f"{subdomain}, Status: 404, URL: {url}\n")
                is_vulnerable = True

            if is_vulnerable:
                break

        except requests.exceptions.RequestException as e:
            print(f"Error reaching {subdomain} via {protocol}: {e}")
            output_file.write(f"{subdomain}, Error: {e}, Protocol: {protocol}\n")
    
    return is_vulnerable

def analyze_subdomain(subdomain, output_file):
    print(f"\nAnalyzing {subdomain}...")
    dns_info = resolve_dns(subdomain)
    ssl_info = check_ssl(subdomain)
    is_vulnerable = check_takeover(subdomain, output_file)
    return {
        "subdomain": subdomain,
        "dns_info": dns_info,
        "ssl_info": ssl_info,
        "vulnerable": is_vulnerable
    }

def analyze_subdomains_from_file(file_path):
    vulnerable_subdomains = []
    with open("vulnerable_subdomains.txt", 'a') as output_file:
        with open(file_path, 'r') as file:
            subdomains = file.readlines()
            for subdomain in subdomains:
                subdomain = subdomain.strip()
                result = analyze_subdomain(subdomain, output_file)
                if result['vulnerable']:
                    vulnerable_subdomains.append(result)
    return vulnerable_subdomains

def generate_report(vulnerable_subdomains):
    report_data = {
        "total_vulnerable": len(vulnerable_subdomains),
        "details": vulnerable_subdomains
    }
    with open("subdomain_report.json", "w") as report_file:
        json.dump(report_data, report_file, indent=4)
    print(f"Report generated: subdomain_report.json")

def main():
    user_input = input("Enter a subdomain or the path to a file containing subdomains: ").strip()

    # تحقق مما إذا كان الإدخال ملفًا أو سب دومينًا مباشرًا
    if os.path.isfile(user_input):
        print(f"File detected. Analyzing subdomains from file: {user_input}")
        vulnerable_subdomains = analyze_subdomains_from_file(user_input)
    else:
        print(f"Analyzing single subdomain: {user_input}")
        with open("vulnerable_subdomains.txt", 'a') as output_file:
            result = analyze_subdomain(user_input, output_file)
            vulnerable_subdomains = [result] if result['vulnerable'] else []

    generate_report(vulnerable_subdomains)
    print("Analysis complete.")

if __name__ == "__main__":
    main()
