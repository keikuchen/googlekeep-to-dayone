import json
import os
from datetime import datetime


def convert_google_keep_to_day_one(keep_folder_path, day_one_json_file):
    day_one_entries = []

    for filename in os.listdir(keep_folder_path):
        if filename.endswith(".json"):
            with open(
                os.path.join(keep_folder_path, filename), "r", encoding="utf-8"
            ) as keep_file:
                note = json.load(keep_file)

            title = note.get("title", "")
            content = note.get("textContent", "")

            created_time = note.get("createdTimestampUsec", "")
            if created_time:
                created_time = datetime.fromtimestamp(
                    created_time / 1000000
                ).isoformat()

            modified_time = note.get("userEditedTimestampUsec", "")
            if modified_time:
                modified_time = datetime.fromtimestamp(
                    modified_time / 1000000
                ).isoformat()

            labels = note.get("labels", [])
            label_names = [label.get("name") for label in labels]

            day_one_entry = {
                "creationDate": created_time,
                "modifiedDate": modified_time,
                "title": title,
                "text": content,
                "tags": label_names,  # Add tags if needed
            }
            day_one_entries.append(day_one_entry)

    with open(day_one_json_file, "w", encoding="utf-8") as day_one_file:
        json.dump(day_one_entries, day_one_file, ensure_ascii=False, indent=4)

    print("Conversion completed successfully.")


# Google Keepエントリーフォルダのパス
keep_folder_path = "keep_entries_folder"
# Day OneにインポートするJSONファイルのパス
day_one_json_file = "day_one_entries.json"

# Google KeepからDay Oneに変換
convert_google_keep_to_day_one(keep_folder_path, day_one_json_file)
