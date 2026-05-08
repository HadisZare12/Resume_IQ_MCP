
from apify_client import ApifyClient
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
apify_client = ApifyClient(os.getenv("APIFY_TOKEN_KEY"))

def fetch_linkedin_jobs(search_query, location="germany", rows=10):
    run_input = {
        "keyword": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    
    print("LINKEDIN RUN KEYS:", run.keys())  
    print("LINKEDIN RUN:", run)             
    
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_xing_jobs(location="germany"):
    
    # Prepare the Actor input
    run_input = {
        "startUrl":"",
        "keyword": location,
        "discipline": "Technology",
        "results_wanted": 10,
        "max_pages": 10,
    }

    # Run the Actor and wait for it to finish
    run = apify_client.actor("YGO6eh6ICQXnan9L4").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
