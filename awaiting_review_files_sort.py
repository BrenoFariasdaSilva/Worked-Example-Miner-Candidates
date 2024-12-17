## How to Run:
# Linux/Mac: python3 awaiting_review_files_sort.py
# Windows: python awaiting_review_files_sort.py

import os # Library for file and directory operations
import re # Library for working with regular expressions
import shutil # Library for file and directory movement

REGEX = r"^([^_]+)_" # Regular expression to capture the repository name before the first underscore
PATH = "./candidates/awaiting_review/" # Path to the directory where the script operates

def create_directory(repo_name: str) -> None:
	"""
	Create a directory for the repository if it does not exist.

	param repo_name (str): Name of the repository directory to create.
	return None
	"""

	if not os.path.exists(os.path.join(PATH, repo_name)): # Check if the directory already exists
		os.makedirs(os.path.join(PATH, repo_name)) # Create the directory
		print(f"Directory created: {repo_name}") # Print a message to the console

def move_files_to_directory(repo_name: str) -> None:
	"""
	Move all files that start with the repository name and end with ".csv" into the directory.

	param repo_name (str): Name of the repository directory to move files into.
	return None
	"""

	for file in os.listdir(PATH): # Iterate over all files in the specified directory
		if file.startswith(repo_name) and file.endswith(".csv"): # Check if the file matches the repository name and is a CSV file
			shutil.move(os.path.join(PATH, file), os.path.join(PATH, repo_name, file)) # Move the file into the repository directory
			print(f"File moved: {file} -> {repo_name}/") # Print a message to the console

def process_csv_files() -> None:
	"""
	Process all CSV files in the specified directory:
	- Extract the repository name.
	- Create a directory named after the repository.
	- Move matching files into the respective directory.

	param None
	return None
	"""

	for filename in os.listdir(PATH): # Iterate over all files in the specified directory
		if filename.endswith(".csv"): # Check if the file is a CSV file
			match = re.match(REGEX, filename) # Match the regular expression with the filename
			if match: # Check if the regular expression matched
				repo_name = match.group(1) # Extract the repository name
				create_directory(repo_name) # Create the directory for the repository
				move_files_to_directory(repo_name) # Move the files into the repository directory

def main() -> None:
	"""
	Main function to initiate the script"s workflow.
	"""

	print("Organizing the Awaiting Review files in subdirectories according to the repository name...") # Print a message to the console
	process_csv_files() # Process all CSV files in the specified directory
	print("\nProcess completed!") # Print a message to the console

if __name__ == "__main__":
	main() # Execute the main function
