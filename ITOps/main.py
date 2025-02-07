import json
import requests

# Ollama API URL
OLLAMA_API_URL = "http://localhost:11433/api/generate"

def load_json(file_path):
    with open(file_path, "r") as file:
        incident_data = json.load(file)
    return print(incident_data)

def analyse_incident(incident):
    """Send incident data to Ollama for analysis and get recommendations."""
    
    # Define the prompt template
    prompt_template = """
    Analyse the following IT incident data and provide a summary along with recommendations,
    based on previous incidents and best practices.

    Incident ID: 1002
    Title: Issue with database connection
    Description: LAMP server unable to connect to MySQL database after server upgrade
    Criticality: P2
    Date Created: 2022-10-15 08:30:00
    Date Resolved: NA
    Engineer: Suhail
    Team: Managed Services
    Status: In-Porgress

    ### Tasks:
    1. Summarize the issue and its resolution.
    2. Identify potential causes based on the description.
    3. Provide recommendations to prevent similar incidents in the future.
    """

    prompt = prompt_template.format(**incident)

    payload = {
        "model": "llama3:latest",  # Ensure this is the correct model
        "prompt": prompt,
        "stream": False,
        "max_tokens": 300  # Limit output to prevent large responses
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as execption:
        return f"Request failed: {str(execption)}"

def process_incidents(file_path, limit=10):
    import json
    
    def load_json(file_path):
        try:
            with open(file_path, "r") as file:
                incident_data = json.load(file)
            return incident_data
        except Exception as e:
            print(f"Error loading JSON data: {e}")
            return None
    
    incident_data = load_json(file_path)
    if incident_data is not None:
        responses = []
        for incident in incident_data[:limit]:
            recommendation = analyse_incident(incident)
            responses.append({
                "Incident ID": incident["Incident ID"],
                "Title": incident["Issue Title"],
                "Recommendation": recommendation
            })
            print(f"✅ Processed Incident {incident['Incident ID']}")

        # Save recommendations to a file
        output_file = "incident_recommendations.json"
        with open(output_file, "w") as file:
            json.dump(responses, file, indent=4)

        print(f"\n📂 Recommendations saved to {output_file}")
    else:
        print("No incident data to process.")
import json

def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            incident_data = json.load(file)
        return incident_data
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return None

def process_incidents(file_path, limit):
    incident_data = load_json(file_path)
    if incident_data is not None:
        responses = []
        for incident in incident_data[:limit]:
            recommendation = analyse_incident(incident)
            responses.append({
                "Incident ID": incident["Incident ID"],
                "Title": incident["Issue Title"],
                "Recommendation": recommendation
            })
            print(f"✅ Processed Incident {incident['Incident ID']}")

        # Save recommendations to a file
        output_file = "incident_recommendations.json"
        with open(output_file, "w") as file:
            json.dump(responses, file, indent=4)

        print(f"\n📂 Recommendations saved to {output_file}")
    else:
        print("No incident data to process.")

if __name__ == '__main__':
    process_incidents('data.json', limit=10)