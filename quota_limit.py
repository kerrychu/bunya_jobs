import os
from dotenv import load_dotenv
from utils.subprocess_operations import get_piped_stdout, stdout_to_quota_records
from hooks.slack import send_slack_message

load_dotenv()

PROJECT_IDs: list[str] = os.getenv("PROJECT_IDS").split(',')
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
        file_set = {"FileSet": project_id}
        data = {**file_set, **quota_record}
        send_slack_message(data=data, webhook=SLACK_WEBHOOK)


if __name__ == "__main__":
    monitor()