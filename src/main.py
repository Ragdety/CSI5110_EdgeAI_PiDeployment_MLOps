import argparse
import os

from dotenv import load_dotenv, set_key
from mlops.edge_impulse_client import EdgeImpulseClient

# Load environment variables from .env file
load_dotenv()

def setup(project_id, api_key, deploy_type):
    """
    Save the Edge Impulse setup configuration in a .env file.
    """
    set_key(".env", "EI_PROJECT_ID", str(project_id))
    set_key(".env", "EI_API_KEY", api_key)
    set_key(".env", "DEPLOY_TYPE", deploy_type)
    print("Configuration saved successfully.")

def main():
    parser = argparse.ArgumentParser(description="Edge Impulse CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Setup command
    parser_setup = subparsers.add_parser("setup", help="Set up the CLI tool")
    parser_setup.add_argument("--project_id", type=int, required=True, help="Edge Impulse Project ID")
    parser_setup.add_argument("--api_key", type=str, required=True, help="Edge Impulse API Key")
    parser_setup.add_argument("--deploy_type", type=str, required=True, help="Deployment type (e.g., zip)")

    # Build command
    subparsers.add_parser("build", help="Build the Edge Impulse model")

    # Wait for job completion command
    parser_wait = subparsers.add_parser("wait_for_job_completion", help="Wait for job completion")
    parser_wait.add_argument("--job_id", type=str, required=True, help="Job ID to monitor")

    # Deploy command
    subparsers.add_parser("deploy_model", help="Deploy the Edge Impulse model")

    args = parser.parse_args()

    ei_project_id = os.getenv("EI_PROJECT_ID")
    ei_api_key = os.getenv("EI_API_KEY")
    deploy_type = os.getenv("DEPLOY_TYPE", "zip")

    if args.command == "setup":
        setup(args.project_id, args.api_key, args.deploy_type)
    elif args.command == "build":
        if not ei_project_id or not ei_api_key:
            raise Exception("Setup is required. Run 'setup' command first.")
        
        client = EdgeImpulseClient(ei_project_id, ei_api_key, deploy_type)
        job_id = client.build()
        print(f"Build started. Job ID: {job_id}")
    elif args.command == "wait_for_job_completion":
        if not ei_project_id or not ei_api_key:
            raise Exception("Setup is required. Run 'setup' command first.")
        
        client = EdgeImpulseClient(ei_project_id, ei_api_key, deploy_type)
        client.wait_for_job_completion(args.job_id)
        print("Build job completed.")
    elif args.command == "deploy_model":
        if not ei_project_id or not ei_api_key:
            raise Exception("Setup is required. Run 'setup' command first.")
        
        client = EdgeImpulseClient(ei_project_id, ei_api_key, deploy_type)
        fname, bin_file = client.download_model()

        with open(fname, "wb") as f:
            f.write(bin_file)
        print(f"Model downloaded as {fname}.")

if __name__ == "__main__":
    main()
    