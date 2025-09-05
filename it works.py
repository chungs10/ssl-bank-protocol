import requests
import json

# API endpoint and parameters
api_base_url = "https://xivapi.com/item/"
api_params = "?columns=Name,Description,DamagePhys,DamageMag,Stats,LevelItem&private_key=d41321754a094221ab1e0d26eb1909b30c867e847a3146cb962a3f144fb00182"
num_times = 39100 + 200  # Number of times to call the API

# Function to fetch data from the API and create documents
def fetch_and_create_documents(api_base_url, api_params, num_times):
    documents = []

    for item_number in range(39100, num_times + 1):
        api_url = f"{api_base_url}{item_number}{api_params}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            # Add both original and adjusted item numbers
            data["o_item_number"] = item_number
            data["a_item_number"] = item_number - 39099
            documents.append(data)
            print("Fetched document:", data)
        else:
            print(f"Failed to fetch data for item {item_number} from API:", response.status_code)

    return documents

if __name__ == "__main__":
    documents = fetch_and_create_documents(api_base_url, api_params, num_times)
    
    # Save all documents into one JSON file
    output_filename = "all_documents.json"
    with open(output_filename, "w") as json_file:
        json.dump(documents, json_file, indent=4)
    print(f"All documents saved to {output_filename}")
