#!/bin/bash

# Apply black formatter
black $(git ls-files '*.py')

# Sort imports
isort ./app

# Remove unused imports and variables
autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports $(git ls-files '*.py')
