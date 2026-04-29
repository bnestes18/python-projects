from dotenv import load_dotenv
from os import getenv
# Set application log level
logging.basicConfig(level=logging.INFO)

# Load .env file, if exists
load_dotenv()

DEFAULT_LIMIT = 10
DEFAULT_TOP_N = 3
DEFAULT_OUTPUT = "table"

# Resolves token when referenced on the commandline, or in a .env file
def resolve_token(cli_token: str | None) -> str:
    token = cli_token or getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("No GitHub token found. Set GITHUB_TOKEN env variable or pass --token flag")
    return token