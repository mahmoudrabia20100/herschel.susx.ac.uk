import sublist3r

def get_subdomains(domain):
    try:
        print(f"Finding subdomains for: {domain}")

        # Perform deep subdomain search by enabling brute force and using all available engines
        subdomains = sublist3r.main(
            domain, 
            40, 
            f"{domain}_subdomains.txt", 
            ports=None, 
            silent=True, 
            verbose=True,  # Set to True for more output during the search
            enable_bruteforce=True,  # Enable brute force for deeper search
            engines=None  # Use all available engines for maximum coverage
        )
        
        if subdomains:
            print(f"Found {len(subdomains)} subdomains:")

            # Save subdomains to a text file
            filename = f"{domain}_subdomains.txt"
            with open(filename, "w") as file:
                for subdomain in subdomains:
                    print(subdomain)  # Print to console
                    file.write(subdomain + "\n")  # Save subdomains to the text file
            print(f"Subdomains have been saved to {filename}")
        else:
            print("No subdomains found.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
domain = input("Enter the domain (e.g., example.com): ")
get_subdomains(domain)
