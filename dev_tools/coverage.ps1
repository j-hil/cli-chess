# script to run coverage.py then print & generate the report.
coverage run -m unittest discover -s ./tests -p test_*.py
coverage report
coverage html