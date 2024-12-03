import requests

response = requests.get(
    "https://studio.edgeimpulse.com/v1/api/{projectId}/deployment/targets",
    headers={},
)
data = response.json()


class EdgeImpulseDeployer:
    api_base_url = "https://studio.edgeimpulse.com/v1/api"

    def __init__(self, project_id):
        self.project_id = project_id

    def deploy(self):
        response = requests.post(
            f'{self.api_base_url}/{self.project_id}/deployment',
            headers={},
        )
        return response.json()
    
    def get_targets(self):
        response = requests.get(
            f'{self.api_base_url}/{self.project_id}/deployment/targets',
            headers={},
        )
        return response.json()