import csv # For reading and writing CSV files
import os # For running a command in the terminal
import re # For regular expressions
from colorama import Style # For coloring the terminal
from datetime import datetime # This module supplies classes for manipulating dates and times.

# Macros:
class BackgroundColors: # Colors for the terminal
   CYAN = "\033[96m" # Cyan
   GREEN = "\033[92m" # Green
   YELLOW = "\033[93m" # Yellow
   RED = "\033[91m" # Red
   BOLD = "\033[1m" # Bold
   UNDERLINE = "\033[4m" # Underline
   CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Execution Constants:
VERBOSE = False # Set to True to output verbose messages

def verbose_output(true_string="", false_string=""):
   """
   Outputs a message if the VERBOSE constant is set to True.

   :param true_string: The string to be outputted if the VERBOSE constant is set to True.
   :param false_string: The string to be outputted if the VERBOSE constant is set to False.
   :return: None
   """

   if VERBOSE and true_string != "": # If the VERBOSE constant is set to True and the true_string is set
      print(true_string) # Output the true statement string
   elif false_string != "": # If the false_string is set
      print(false_string) # Output the false statement string

def verify_filepath_exists(filepath):
   """
   Verify if a file or folder exists at the specified path.

   :param filepath: Path to the file or folder
   :return: True if the file or folder exists, False otherwise
   """

   verbose_output(f"{BackgroundColors.YELLOW}Verifying if the file or folder exists at the path: {BackgroundColors.CYAN}{filepath}{Style.RESET_ALL}") # Output the verbose message

   return os.path.exists(filepath) # Return True if the file or folder exists, False otherwise

def get_timestamp():
   """
   Generates the current timestamp.

   :return: The current timestamp in the format YYYY-MM-DD HH:MM:SS
   """

   return datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Return the current timestamp

def get_markdown_header(timestamp):
   """
   Generates the header for the markdown table.

   :param timestamp: The timestamp to include in the header
   :return: List of markdown header lines
   """

   return [
      f"### Candidates Summary (Last Updated: {timestamp})\n",
      "| # | Status | Repo Name | Class Candidates | Method Candidates |",
      "|---|--------|----------|------------------|------------------|"
   ]

def get_base_dirs(candidates_path):
   """
   Retrieves the base directories inside the candidates directory.

   :param candidates_path: Path to the candidates directory
   :return: List of base directories
   """
   
   return [d for d in os.listdir(candidates_path) if os.path.isdir(os.path.join(candidates_path, d))]

def get_repo_dirs(status_path):
   """
   Retrieves repository directories inside a given status directory.

   :param status_path: Path to the status directory
   :return: List of repository directories
   """

   return [repo for repo in os.listdir(status_path) if os.path.isdir(os.path.join(status_path, repo))]

def count_candidates(file_path):
   """
   Counts the number of non-empty candidate lines in a CSV file after the header.

   :param file_path: Path to the CSV file
   :return: The number of non-empty candidate lines in the CSV file after the header
   """

   verbose_output(f"{BackgroundColors.YELLOW}Counting candidates in the CSV file: {BackgroundColors.CYAN}{file_path}{Style.RESET_ALL}") # Output the verbose message

   try: # Try to read the CSV file
      with open(file_path, newline="", encoding="utf-8") as csvfile: # Open the CSV file
         reader = csv.reader(csvfile) # Create a CSV reader
         rows = [row for row in reader if any(cell.strip() for cell in row)] # Ignore empty lines
         return max(0, len(rows) - 1) # Subtract header row
   except Exception as e: # Catch any exceptions
      print(f"Error reading {file_path}: {e}") # Output the error message
      return 0 # Return 0

def count_csv_candidates(repo_path, repo_name):
   """
   Counts the number of class and method candidates in the repository CSV files.

   :param repo_path: Path to the repository directory
   :param repo_name: Name of the repository
   :return: Tuple (class_count, method_count)
   """

   class_csv = os.path.join(repo_path, f"{repo_name}_classes_candidates.csv") # Get the path to the classes CSV file
   method_csv = os.path.join(repo_path, f"{repo_name}_methods_candidates.csv") # Get the path to the methods CSV file
   
   class_count = count_candidates(class_csv) if os.path.exists(class_csv) else 0 # Count the number of class candidates
   method_count = count_candidates(method_csv) if os.path.exists(method_csv) else 0 # Count the number of method candidates
   
   return class_count, method_count # Return the class and method counts

def get_table_rows(candidates_path):
   """
   Generates the rows of the table, collecting status, repo name, and candidate counts.

   :param candidates_path: Path to the candidates directory
   :return: List of table rows with status, repo name, class candidates, and method candidates
   """

   table_rows = [] # List of table rows
   base_dirs = get_base_dirs(candidates_path) # Get the base directories inside the candidates directory

   for status in base_dirs: # Iterate through the base directories
      status_path = os.path.join(candidates_path, status) # Get the path to the status directory

      for repo_name in get_repo_dirs(status_path): # Iterate through the repository directories
         repo_path = os.path.join(status_path, repo_name) # Get the path to the repository directory
         class_count, method_count = count_csv_candidates(repo_path, repo_name) # Count the class and method candidates

         table_rows.append((status, repo_name, class_count, method_count)) # Store data for sorting

   return table_rows # Return the table rows

def sort_table_rows(table_rows):
   """
   Sorts the table rows by Status and Repo Name.

   :param table_rows: List of table rows
   :return: List of sorted table rows
   """

   return sorted(table_rows, key=lambda x: (x[0], x[1].lower())) # Sort first by "Status", then by "Repo Name"

def generate_markdown():
   """
   Generates a markdown table with candidate counts for each repository, 
   sorted by Status and Repo Name.

   :param None
   :return: List of markdown lines
   """

   verbose_output(f"{BackgroundColors.YELLOW}Generating markdown table with candidate counts for each repository{Style.RESET_ALL}")

   candidates_path = os.path.join(os.getcwd(), "candidates") # Get the path to the candidates directory
   timestamp = get_timestamp() # Get the current timestamp

   markdown_lines = get_markdown_header(timestamp) # Get the markdown header lines
   table_rows = get_table_rows(candidates_path) # Get the table rows

   table_rows = sort_table_rows(table_rows) # Sort the table rows

   for i, (status, repo_name, class_count, method_count) in enumerate(table_rows, start = 1): # Iterate through the sorted table rows
      markdown_lines.append(f"| {i} | {status} | {repo_name} | {class_count} | {method_count} |") # Append the table row to the markdown lines

   return markdown_lines # Return the markdown lines

def read_readme(file_path):
   """
   Reads the content of README.md.

   :param file_path: Path to the README.md file
   :return: Content of the file as a string
   """

   verbose_output(f"{BackgroundColors.YELLOW}Reading the README.md file{Style.RESET_ALL}") # Output the verbose message

   with open(file_path, "r", encoding="utf-8") as file: # Open the README.md file
      return file.read() # Return the content of the file

def construct_table(markdown_lines, start_marker, end_marker):
   """
   Constructs the new markdown table within the placeholder tags.

   :param markdown_lines: List of markdown lines
   :param start_marker: Start placeholder tag
   :param end_marker: End placeholder tag
   :return: Formatted table content
   """

   verbose_output(f"{BackgroundColors.YELLOW}Constructing the new markdown table within the placeholder tags{Style.RESET_ALL}")
   
   return f"{start_marker}\n\n" + "\n".join(markdown_lines) + f"\n\n{end_marker}" # Return the formatted table content

def replace_table(content, new_table, start_marker, end_marker):
   """
   Replaces the existing markdown table within the placeholder tags.

   :param content: Original README.md content
   :param new_table: New markdown table content
   :param start_marker: Start placeholder tag
   :param end_marker: End placeholder tag
   :return: Updated README.md content
   """

   verbose_output(f"{BackgroundColors.YELLOW}Replacing the existing markdown table within the placeholder tags{Style.RESET_ALL}")

   table_pattern = re.compile(
      f"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
      re.DOTALL
   ) # Regular expression pattern for the table

   if table_pattern.search(content): # If the table pattern is found
      return table_pattern.sub(new_table, content) # Replace the table with the new table
   
   print("{BackgroundColors.RED}Table pattern not found in README.md{Style.RESET_ALL}") # Output the error message

   return None # Return None

def write_readme(file_path, content):
   """
   Writes the updated content back to README.md.

   :param file_path: Path to the README.md file
   :param content: Updated content
   """

   verbose_output(f"{BackgroundColors.YELLOW}Writing the updated content back to README.md{Style.RESET_ALL}")

   with open(file_path, "w", encoding="utf-8") as file: # Open the README.md file
      file.write(content) # Write the updated content

def update_readme(markdown_lines):
   """
   Updates the README.md file by replacing the markdown table inside the placeholder tags.

   :param markdown_lines: List of markdown lines
   :return: None
   """

   verbose_output(f"{BackgroundColors.YELLOW}Updating the README.md file with the new markdown table{Style.RESET_ALL}")

   readme_path = "./README.md" # Path to the README.md file
   start_marker = "<!-- START README-CANDIDATES-TABLE -->" # Start placeholder tag
   end_marker = "<!-- END README-CANDIDATES-TABLE -->" # End placeholder tag

   readme_content = read_readme(readme_path) # Read the README.md file
   new_table_content = construct_table(markdown_lines, start_marker, end_marker) # Construct the new markdown table
   updated_readme_content = replace_table(readme_content, new_table_content, start_marker, end_marker) # Replace the existing markdown table with the new markdown table

   if updated_readme_content: # If the updated README.md content is not None
      write_readme(readme_path, updated_readme_content) # Write the updated content back to README.md
      verbose_output(f"{BackgroundColors.GREEN}README.md updated successfully{Style.RESET_ALL}") # Output the success message

def main():
   """
   Main function.

   :return: None
   """

   print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Candidates Summary Table Generator{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the Welcome message

   markdown_lines = generate_markdown() # Generate the markdown table
   update_readme(markdown_lines) # Update the README.md file with the new markdown table

   print(f"\n{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """

   main() # Call the main function
