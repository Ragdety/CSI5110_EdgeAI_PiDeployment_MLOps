import argparse

from mlops.edge_impulse_client import EdgeImpulseClient



def main():
    parser = argparse.ArgumentParser(description="Edge Impulse CLI Tool")

    parser.add_argument("project_id", type=int, help="Project ID")
    parser.add_argument("api_key", type=str, help="API Key")
    parser.add_argument("--deploy_type", type=str, default="zip", help="Deployment type (default: zip)")

    args = parser.parse_args()

    client = EdgeImpulseClient(args.project_id, args.api_key, args.deploy_type)

    try:
        job_id = client.build_model()
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




if __name__ == "__main__":
    main()

