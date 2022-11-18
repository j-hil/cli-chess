# script to run coverage.py then print & generate the report.
coverage run -m pytest ./tests
coverage report
coverage html
