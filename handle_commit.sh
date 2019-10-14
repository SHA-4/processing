#!/bin/bash
# Based on http://sweetme.at/2013/09/26/automate-your-git-directory-initialization-workflow/

if [ ! -d ".git" ]; then
  git init
  if (( $? )); then
      echo "Unable to initialize your directory"
      exit 1
  fi
fi

git add .
if (( $? )); then
echo "Unable to stage files"
exit 1
fi

git commit -m "$1"
if (( $? )); then
echo "Unable to commit"
exit 1
fi

exit 0

