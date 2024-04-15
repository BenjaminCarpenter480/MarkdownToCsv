Program for converting a folder of markdown files into a collection of csv line entries that can
 then be uploaded to tempo

Notes are formatted following the rules: 
    -All time-sheet entries for a day are in a single directory where the directory name is the date of those entries with YYYY-MM-DD format
    -Each file in a folder is a different worklog entry
    -The first 4 characters of the file name are the start time of the entry formatted as HHMM
    -The rest of the file name is a summary of the work log
    -Each file contains a collection of file properties listed below:
        -Tags: this can be ignored
        -Issue: The issue that the worklog relates to 
        -Date: The datetime which this file was created
        -Start Time: The time work started
        -End Time: The time work finished
        -Time Spent: The amount of time worked (End time - start time) with format "XhYm"
        -The rest of the file is the worklog description

The data will be read into python, do some formatting and then written to a csv file. 
The csv file will have headers: Project Name,Project Key,Issue Key,Summary,Worklog,Project Type

Project Name: the Issue entry of the properties before the "-"
Project Key:the Issue entry of the properties before the "-"
Issue: the Issue entry of the properties
Summary: the rest of the file name defined as the summary
Worklog: Made up of 4 parts separated by the ';' character. 
        The 4 sections are the Worklog description, Worklog date, Worklog author (username), Worked seconds 
The Project Type is 'software'


An example worklog file is "/home/benjamin/Desktop/Obsidian/Personal/Work/Daily Notes/2024-04-11/1100 Looking at running TDCS std commands test without the error causing parts.md"
