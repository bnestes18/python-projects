import httpx
import os
from dotenv import load_dotenv 
import logging
import utils

logger = logging.getLogger("Logger")

# Load .env file, if exists
load_dotenv()

class GitHubClient:
    def __init__(self, token: str):
        # Validate token
        if not token:
            raise ValueError("Missing or invalid api token.")
        if not isinstance(token, str):
            raise TypeError("Token parameter must be a string.")
        self.token = token
        self.headers = {
            "Authorization": "Bearer " + self.token, # Apply 'Authorization: token' header if using GitHub token, otherwise 'Authorization: Bearer {token}' if using JWT.
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.client = httpx.Client(base_url = "https://api.github.com", headers=self.headers)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close() # Close client connection
        return False

    def get_workflow_runs(self, owner: str, repo: str, limit: int) -> list[dict]:

        # TODO implement retries and timeouts
        try:
            response = self.client.get(f"/repos/{owner}/{repo}/actions/runs", params={"per_page": limit})
            response.raise_for_status()
            data = response.json()
            return data["workflow_runs"]
        except httpx.HTTPStatusError as e:
            utils.handle_http_error(e, "Failed to retrieve workflow runs")
        except httpx.RequestError as e: 
            utils.handle_http_error(e, "Network error occurred while retrieving workflow runs")

    def get_jobs_for_run(self, owner: str, repo: str, run_id: int) -> list[dict]:
        return self._paginate(f"/repos/{owner}/{repo}/actions/runs/{run_id}/jobs", key="jobs")

    def _paginate(self, url: str, key: str) -> list[dict]:
        results = []
        next_link_url = url
        while next_link_url:
            try:
                response = self.client.get(next_link_url)
                response.raise_for_status()
                data = response.json()
                # Check if specified key exists in response data. If not, raise an error
                if key not in data:
                    logger.error(f"specified key '{key}' not found in response data. Available keys are: {list(data.keys())}")
                    raise KeyError("Cannot paginate results.")
                # else, use provided key to extract desired response data
                results.extend(data[key])
                next_link_url = response.links.get("next", {}).get("url")
            except httpx.HTTPStatusError as e:
                utils.handle_http_error(e, "Bad response during pagination")
            except httpx.RequestError as e: 
                utils.handle_http_error(e, "Network error occurred during pagination")
        logger.info("Pagination complete")
        return results
        
# Runs only when script is executed
if __name__ == "__main__":
    with GitHubClient(os.getenv("GITHUB_TOKEN")) as client:
        runs = client.get_workflow_runs('bnestes18', 'pyweather', 30)
        jobs = client.get_jobs_for_run('bnestes18', 'pyweather', runs[0]["id"])