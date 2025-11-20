#!/bin/bash
cd /home/kavia/workspace/code-generation/personal-notes-manager-209752-209765/backend_flask
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

