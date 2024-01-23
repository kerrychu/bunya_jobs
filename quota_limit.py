import os
from dotenv import load_dotenv
from utils.subprocess_operations import get_piped_stdout, stdout_to_quota_records
from hooks.slack import send_slack_message

load_dotenv()

PROJECT_IDs: list[str] = os.getenv("PROJECT_IDS").split(",")
SLACK_WEBHOOK: str = os.getenv("SLACK_QUOTA_WEBHOOK")


def get_fileset_quota(project_id: str) -> str:
    main_cmd = "rquota"
    piped_cmd = f"grep {project_id}"

    stdout: str = get_piped_stdout(main_command=main_cmd, piped_command=piped_cmd)
    return stdout


def monitor():
    for project_id in PROJECT_IDs:
        raw_quota = get_fileset_quota(project_id)
        quota_record = stdout_to_quota_records(raw_quota)
        slack_message = ""
        for key, value in quota_record.items():
            slack_message += f"⦿ {key}: {value}\n"

        send_slack_message(message=slack_message, webhook=SLACK_WEBHOOK)


if __name__ == "__main__":
    monitor()
