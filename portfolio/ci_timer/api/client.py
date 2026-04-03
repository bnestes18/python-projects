import httpx
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger("Logger")

# Load .env file, if exists
load_dotenv()

class GitHubClient:
    def __init__(self, token: str):
        # Validate token
        if not token:
            raise Exception("Missing api token parameter.")
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
        # GET /repos/{owner}/{repo}/actions/runs
        # raise a clear RuntimeError if status != 200
        # return response["workflow_runs"]
        runs_url = f'/repos/{owner}/{repo}/actions/runs'

        # TODO implement retries and timeouts
        try:
            response = self.client.get(runs_url, headers=self.headers, params={"per_page": limit})
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logging.critical(f"Failed to retrieve workflow runs: {e}")
        
        data = response.json()
        return data["workflow_runs"]

    def get_jobs_for_run(self, owner: str, repo: str, run_id: int) -> list[dict]:
        # GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
        # raise a clear error if status != 200
        # return response["jobs"]
        # NOTE: the API paginates at 30 by default — handle this
        jobs_url = f'/repos/{owner}/{repo}/actions/runs/{run_id}/jobs'
        return self._paginate(jobs_url, key="jobs")

    def _paginate(self, url: str, key: str) -> list[dict]:
        # GitHub uses Link headers for pagination
        # loop: fetch page, collect results, check for "next" in Link header
        # return all accumulated results
        # this will be called by get_jobs_for_run
        results = []
        next_link_url = url
        while next_link_url:
            response = self.client.get(next_link_url, headers=self.headers)
            data = response.json()
            # Check if specified key exists in response data. If not, raise an error
            if key not in data:
                logger.error(f"specified key '{key}' not found in response data. Available keys are: {list(data.keys())}")
                raise Exception("Cannot paginate results.")
            # else, use provided key to extract desired response data
            results.extend(data[key])
            next_link_url = response.links.get("next", {}).get("url")
        logger.info("Pagination complete")
        return results
        
# Runs only when script is executed
if __name__ == "__main__":
    with GitHubClient(os.getenv("GITHUB_TOKEN")) as client:
        runs = client.get_workflow_runs('bnestes18', 'pyweather', 30)
        jobs = client.get_jobs_for_run('bnestes18', 'pyweather', runs[0]["id"])