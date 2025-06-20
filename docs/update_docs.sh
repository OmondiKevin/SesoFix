#!/bin/bash

# Build the documentation
make html

# Create the html directory if it doesn't exist
mkdir -p html

# Copy the generated HTML files to the html directory
cp -r build/html/* html/

echo "Documentation updated successfully!"
echo "You can view the documentation by opening docs/html/index.html in a web browser."