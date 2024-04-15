# MarkdownToCSV
Program for converting a folder of markdown worklogs into a collection of csv line entries that can
 then be uploaded to tempo

## Notes are formatted following the rules: 
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

## Output
The data will be read into python, do some formatting and then written to a csv file. 
The csv file will have headers: Project Name,Project Key,Issue Key,Summary,Worklog,Project Type

Project Name: the Issue entry of the properties before the "-"
Project Key:the Issue entry of the properties before the "-"
Issue: the Issue entry of the properties
Summary: the rest of the file name defined as the summary
Worklog: Made up of 4 parts separated by the ';' character. 
        The 4 sections are the Worklog description, Worklog date, Worklog author (username), Worked seconds 
The Project Type is 'software'


## Example worklog and conversion follows

```
2024-11-01/error state testing.md
---
tags: 
Issue: issue-42
Start time: 10:15
End time: 10:45
Time spent: 
Date: 2024-11-01 10:15
---
Working on a different test, it occasionally enters an error state and needs to be tested to see if it can recover on its own. This test will be written in tcl.

The output would be:
```
Project Name,Project Key,Issue Key,Summary,Worklog,Project Type
error state testing,error state testing,issue-42,error state testing;Working on a different test, it occasionally enters an error state and needs to be tested to see if it can recover on its own.;2024-11-01 10:15;username;1800,software
```

The program will be run with the following command line arguments:
    -The path to the directory containing the worklogs
    -The path to the output csv file
    -The author to be used in the Worklog field
