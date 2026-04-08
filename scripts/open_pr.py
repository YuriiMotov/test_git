import logging
import secrets
import subprocess

from github import Github
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_token: SecretStr
    github_repository: str
    httpx_timeout: int = 30


def main() -> None:
    with open("test.txt", "w+") as f:
        f.write("Hello!")

    settings = Settings()
    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(settings.github_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)


    logging.info("Committing updated file")
    message = "👥 Update FastAPI People - Contributors and Translators"
    subprocess.run(["git", "commit", "-m", message], check=True)

    logging.info("Pushing branch")
    branch_name = f"pr-{secrets.token_hex(4)}"
    subprocess.run(["git", "push", "origin", branch_name], check=True)

    logging.info("Creating PR")
    pr = repo.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")

    logging.info("Finished")


if __name__ == "__main__":
    main()
