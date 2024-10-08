"""
# Log Splitter with Summarization and Markdown Formatting

This Python program processes a CSV file containing logs of issues, work done, and time spent. It reads each log entry, generates a short summary using a pre-trained language model (`czearing/article-title-generator`), and then writes the logs to individual markdown files. Each markdown file is placed inside a folder corresponding to its associated issue. Metadata such as `Log ID`, `Time Spent`, and `Issue Description` are written as front matter in the markdown files, while the worklog details are included in the body.

## Program Workflow:
1. **Read the CSV File**: The program reads a CSV file where each row contains:
   - `Index`: A unique identifier for the log.
   - `Issue`: The issue associated with the log.
   - `Worklog`: A description of the work done.
   - `Logged`: Time spent on the task.
   
2. **Generate Summaries**: Using the `czearing/article-title-generator` model, the program generates a short summary from the `Worklog` field. This summary is used to create a filename for each log file.

3. **Write Markdown Files**: 
   - For each log entry, the program creates a directory (if it doesn't already exist) named after the issue.
   - Inside this directory, a markdown file is created for the log entry. The filename includes the log index and the generated summary.
   - The markdown file includes metadata (front matter) for `Log ID`, `Time Spent`, and `Issue Description`. The body of the markdown contains the `Worklog` content.
   
4. **Efficient Model Usage**: The model and tokenizer are loaded once globally for efficiency and reused during the process.

## Example Markdown Output:
```markdown
---
Log ID: 001
Time Spent: 2 hours
Issue Description: Fix login bug on homepage
---

Investigated the bug in the login flow and updated the authentication logic to prevent multiple requests.
```

## TODOs:
1. **Model Loading Efficiency**: ✅ **DONE**  
   - Load the model and tokenizer only once globally instead of inside the `create_summary` function for better performance.

2. **Error Handling**:  
   - Add more robust error handling for empty rows or invalid CSV data (e.g., missing columns).

3. **File and Directory Handling**:  
   - Improve filename sanitization to handle a broader range of edge cases for special characters.
   - Consider adding safeguards to prevent overwriting files with the same log ID and summary.

4. **Logging**:  
   - Implement logging to track progress, errors, and performance metrics when processing large CSV files.

"""


import os
import csv
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import sys

# Function to create a summary from the log description
def create_summary_bad(description, max_lines=1):
    tokenizer = AutoTokenizer.from_pretrained("czearing/article-title-generator")
    model = AutoModelForSeq2SeqLM.from_pretrained("czearing/article-title-generator")  
    
    summariser = pipeline("summarization", model="czearing/article-title-generator")
    summary = summariser(description,min_length=5)[0]["summary_text"]
    return summary

def create_summary(description, max_lines=1):
    tokenizer = AutoTokenizer.from_pretrained("czearing/article-title-generator")
    model = AutoModelForSeq2SeqLM.from_pretrained("czearing/article-title-generator")  
    
    input_tokens = tokenizer(description, return_tensors="pt").input_ids
    output_ids = model.generate(input_tokens)
    summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return summary

# Function to write each log to its own file
def write_log(issue_dir, log_index, issue_desc, time_spent, summary, log_content):
    # Replace illegal filename characters and create filename
    sanitized_summary = ''.join(e for e in summary if e.isalnum() or e.isspace()).strip()[:50]
    filename = f"{log_index}_{sanitized_summary}.md"
    file_path = os.path.join(issue_dir, filename)

    # Write the log content to a file
    with open(file_path, 'w') as file:
        file.write(f"---\n")
        file.write(f"Log ID: {log_index}\n")
        file.write(f"Time Spent: {time_spent}\n")
        file.write(f"Issue Description: {issue_desc}\n")
        file.write(f"---\n\n")
        file.write(log_content)

# Main function to split logs into separate files
def split_csv_logs(csv_filename):
    # Create an output directory for logs if it doesn't exist
    output_dir = 'logs_by_issue'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            log_index = row['Index']
            issue_desc = row['Issue']
            description_of_work = row['Worklog']
            time_spent = row['Logged']

            # Create a directory for each issue based on its description
            issue_dir = os.path.join(output_dir, issue_desc[:50].strip().replace(' ', '_'))
            if not os.path.exists(issue_dir):
                os.makedirs(issue_dir)

            # Combine the log data for the content of the file
            log_content = f"{description_of_work}"

            # Create a short summary for the filename (first few lines of work description)
            summary = create_summary(description_of_work)

            # Write each log to its own file in the issue directory
            write_log(issue_dir, log_index, issue_desc, time_spent, summary, log_content)

    print(f"Logs have been successfully split and saved to {output_dir}/")

# Example usage
if __name__=="__main__":
    csv_filename = sys.argv[1]    
    split_csv_logs(csv_filename)

