import argparse
import os

from mlops.edge_impulse_client import EdgeImpulseClient
from constants import DEPLOY_TYPES
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Edge Impulse CLI Tool")

    parser.add_argument("--project_id", type=int, help="Edge Impulse Project ID")
    parser.add_argument("--api_key", type=str, help="Edge Impulse API Key")
    parser.add_argument("--deploy_type", type=str, default="zip", help="Deployment type (default: zip)")

    args = parser.parse_args()

    ei_api_key = args.api_key
    ei_project_id = args.project_id

    if not args.project_id or not args.api_key:
        print("Getting project ID and API key from environment variables")
        ei_api_key = os.getenv('EI_API_KEY')
        ei_project_id = os.getenv('EI_PROJECT_ID')
    
    if args.deploy_type not in DEPLOY_TYPES:
        print(f"Invalid deployment type. Supported types: {DEPLOY_TYPES}")
        return

    client = EdgeImpulseClient(ei_project_id, ei_api_key, args.deploy_type)

    try:
        job_id = client.build()
        print("Job ID is", job_id)

        client.wait_for_job_completion(job_id)
        print("Job", job_id, "is finished")
        
        bin_filename, bin_file = client.download_model()
        print("Output file is", len(bin_file), "bytes")

        with open(bin_filename, "wb") as f:
            f.write(bin_file)
        print("Written job output to", bin_filename)
    except Exception as e:
        print("Error:", e)
        # Additional error handling

        raise e





if __name__ == "__main__":
    main()

