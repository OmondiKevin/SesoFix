@echo off

REM Build the documentation
call make.bat html

REM Create the html directory if it doesn't exist
if not exist html mkdir html

REM Copy the generated HTML files to the html directory
xcopy /E /Y build\html\* html\

echo Documentation updated successfully!
echo You can view the documentation by opening docs\html\index.html in a web browser.