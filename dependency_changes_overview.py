
"""
Dependencies Comparison Tool

This script reads dependencies from two separate text files (representing old and new dependencies)
and provides a comparative analysis in the form of an Excel file.

Input:
- Two text files named as `<project>_old.txt` and `<project>_new.txt` in the same directory 
   where `<project>` is specified either as a command line argument or using the `project` variable within the script.
  Each file should list dependencies in the format: <group_id>:<artifact_id>:<version>.

Example `.txt` file content:
    jakarta.servlet:jakarta.servlet-api:6.0.0
    org.projectlombok:lombok:1.18.28
    ... (and so on for other dependencies)

Output:
- An Excel file named `<project>-dependency-overview.xlsx` that showcases the version changes of
  dependencies between the old and new lists. The Excel file will have columns for group id, 
  artifact id, old version, and new version.

Usage:
- python dependency_changes_overview.py [project_name]
  If project_name is not provided as a command line argument, the script uses the `project` 
  variable value.
"""

import pandas as pd
import sys

project = ""

if  len(sys.argv) > 1:
    project = sys.argv[2]
elif not project:
    print("Project name needs to be specified in variable or as a command line argument")
    sys.exit()

with open(f'{project}_old.txt', 'r') as file:
    prev_dependencies = [line.strip() for line in file if line.strip()]

with open(f'{project}_new.txt', 'r') as file:
    new_dependencies = [line.strip() for line in file if line.strip()]

# Parse dependencies into a structured format
def parse_dependencies(dependencies):
    parsed_data = []
    for dep in dependencies:
        if dep.count(":") < 2:
            print("IGNORED:", dep)
            continue
        group_id, rest = dep.split(":", 1)  # Split at the first colon
        artifact, version = rest.rsplit(":", 1)  # Split at the last colon
        parsed_data.append({"group id": group_id, "artifact id": artifact, "version": version})
    return parsed_data

# Create dataframes
df_old = pd.DataFrame(parse_dependencies(prev_dependencies))
df_old.rename(columns={"version": "prev versions"}, inplace=True)

df_new = pd.DataFrame(parse_dependencies(new_dependencies))
df_new.rename(columns={"version": "new version"}, inplace=True)

df_old.drop_duplicates(subset=['group id', 'artifact id', 'prev versions'], inplace=True)
df_new.drop_duplicates(subset=['group id', 'artifact id', 'new version'], inplace=True)

# Merge dataframes based on group_id and artifact id
result = pd.merge(df_old, df_new, on=['group id', 'artifact id'], how='outer')

# Replace NaN values with dash
result.fillna("-", inplace=True)

# Sort by the artifact id column
result = result.sort_values(by=['artifact id', 'group id'])

# Export to Excel
result.to_excel(f'{project}-dependency-overview.xlsx', index=False, engine='openpyxl')
