
import os
import csv
import datetime
import re
import argparse


def convert_notes_to_csv(notes_dir, csv_file, author):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Project Name", "Project Key", "Issue Key", "Summary", "Worklog", "Project Type"])

        for root, dirs, files in os.walk(notes_dir):
            for name in files:
                if name.endswith(".md"):
                    try:
                        with open(os.path.join(root, name), 'r') as f:
                            content = f.read()
                            header = content.split('---')[1]
                            worklog_description = content.split('---')[2]
                            date = datetime.datetime.strptime(re.search(r'Date:(.*)', header).group(1).strip(), "%Y-%m-%d %H:%M")
                            issue = re.search(r'Issue: (.*)', header).group(1).strip()
                            start_time=datetime.datetime.strptime((re.search(r'Start time:(.*)', header).group(1).strip()), "%H:%M")
                            end_time=datetime.datetime.strptime((re.search(r'End time:(.*)',header).group(1).strip()),"%H:%M")
                            time = (end_time-start_time).total_seconds()

                            project_name = issue.split("-")[0]
                            project_key = issue
                            summary = name[5:]
                            worklog = worklog_description.strip()
                            
                            worklog = (";".join([worklog, date.strftime("%Y-%m-%d"), author ,str(time)])).encode('unicode-escape')
                            project_type = 'software'

                            writer.writerow([project_name, project_key, issue, summary, worklog, project_type])
                    except Exception as e:
                        print(f" -- Got error parsing file {name}. error: {e}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert worklog notes to CSV.')
    parser.add_argument('notes_dir',  type=str, help='Path to the directory containing worklogs')
    parser.add_argument('output_file',  type=str, help='Path to the output CSV file')
    parser.add_argument('author',  type=str, help='Username to be used in the Worklog field')

    args = parser.parse_args()

    convert_notes_to_csv(args.notes_dir, args.output_file, args.author)