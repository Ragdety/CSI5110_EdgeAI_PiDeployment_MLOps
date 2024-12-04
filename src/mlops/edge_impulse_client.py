import requests
import json
import time
import re
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

class EdgeImpulseClient:
    base_url = "https://studio.edgeimpulse.com/v1/api"

    def __init__(self, 
                 project_id,
                 api_key, 
                 deploy_type="zip",
                 logging_level=logging.DEBUG):
        """
        Initialize the Edge Impulse Client.
        :param project_id: The project ID from Edge Impulse
        :param api_key: The API key for authentication
        :param deploy_type: The deployment type (default: 'zip')
        """
        self.project_id = project_id
        self.api_key = api_key
        self.deploy_type = deploy_type
        self.headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Logging Configuration
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

    def build(self):
        """
        Start building the model on the Edge Impulse platform.
        :return: Job ID
        """
        self.logger.info("Building Edge Impulse model...")

        url = f"{self.base_url}/{self.project_id}/jobs/build-ondevice-model"

        self.logger.info(f'URL: {url}')

        querystring = {"type": self.deploy_type}
        payload = {"engine": "tflite-eon"}

        self.logger.debug(f'Headers: {self.headers}')

        response = requests.post(url, json=payload, headers=self.headers, params=querystring)
        body = response.json()

        if not body["success"]:
            self.logger.error("Error building model")
            raise Exception(body["error"])
        
        return body["id"]

    def get_stdout(self, job_id, skip_line_no):
        """
        Fetch job output logs.
        :param job_id: Job ID
        :param skip_line_no: Number of lines to skip
        :return: List of output lines
        """
        url = f"{self.base_url}/{self.project_id}/jobs/{job_id}/stdout"
        response = requests.get(url, headers=self.headers)
        body = response.json()

        if not body["success"]:
            self.logger.error("Error fetching job output")
            raise Exception(body["error"])
        
        stdout = body["stdout"][::-1]  # reverse array so it's old -> new

        return [x["data"] for x in stdout[skip_line_no:]]

    def wait_for_job_completion(self, job_id):
        """
        Wait for a job to complete and display its logs.
        :param job_id: Job ID
        """
        skip_line_no = 0
        url = f"{self.base_url}/{self.project_id}/jobs/{job_id}/status"

        while True:
            response = requests.get(url, headers=self.headers)
            body = response.json()
            if not body["success"]:
                raise Exception(body["error"])

            stdout = self.get_stdout(job_id, skip_line_no)
            for line in stdout:
                print(line, end="")
            skip_line_no += len(stdout)

            if "finished" not in body["job"]:
                time.sleep(1)
                continue
            if not body["job"]["finishedSuccessful"]:
                self.logger.error("Job failed")
                raise Exception("Job failed")
            else:
                break

    def download_model(self):
        """
        Download the built model.
        :return: Filename and binary content of the model
        """
        self.logger.info("Downloading Edge Impulse model")

        url = f"{self.base_url}/{self.project_id}/deployment/download"
        querystring = {"type": self.deploy_type}

        response = requests.get(url, headers=self.headers, params=querystring)
        d = response.headers["Content-Disposition"]
        
        fname = re.findall("filename\\*?=(.+)", d)[0].replace("utf-8''", "")
        return fname, response.content