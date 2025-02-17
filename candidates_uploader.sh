#!/bin/bash

# How to Run:
# chmod +x candidates_uploader.sh
# ./candidates_uploader.sh

echo "Adding the Repository Candidates to the Awaiting Review Directory"

for repo in candidates/awaiting_review/*/; do
   repo_name=$(basename "$repo")
   echo "Adding the ${repo_name} Repository Candidates to the Awaiting Review Directory"
   git add "$repo"
   git commit -m "FEAT: Adding the ${repo_name} Repository Candidates"
   git push
   echo "The ${repo_name} Repository Candidates has been added to the Awaiting Review Directory"
done

echo "The Repository Candidates has been added to the Awaiting Review Directory"
