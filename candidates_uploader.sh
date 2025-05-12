#!/bin/bash

# How to Run:
# chmod +x candidates_uploader.sh
# ./candidates_uploader.sh

echo "Adding the Repository Candidates to the Awaiting Review Directory"

for repo in candidates/awaiting_review/*/; do
   repo_name=$(basename "$repo")
   
   # Verify if there are changes in this specific repo folder
   if git status --porcelain "$repo" | grep -q .; then
      echo "Adding the new ${repo_name} Repository Candidates to the Awaiting Review Directory"
      git add "$repo"
      git commit -m "FEAT: Adding the new ${repo_name} Repository Candidates"
      git push
      echo "The ${repo_name} Repository Candidates has been added to the Awaiting Review Directory"
   else
      echo "No changes detected in ${repo_name}, skipping..."
   fi
done

echo "Done processing all Repository Candidates in the Awaiting Review Directory."
