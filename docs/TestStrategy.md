# Unit Testing
---
Each function in both the front-end and back-end sections of the system will have dedicated tests to ensure system-wide functionality and to detect and address errors.

## CSV Upload Test
---
Test Data strategy:  Uploading Files - is it a CSV? 

This program can only read CSVs, so we’d first have to test if the file being uploaded is a csv

## CSV Read Test
---
Test Data strategy:  Uploading Files - different types of CSVs (different formats) 
Tested as a mock as if the user is uploading a file > The program depends on the data in the CSV, so ensuring that the information in the CSV is actually being read is something that has to be tested. CSVs come in all formats so we’d have to test those first to ensure compatibility before users encounter a problem

## Front End Display
---
Test Data strategy:  Uploading mock CSV File
We want to make sure that the data we want to present is showing up to the user as we intended: uniform, straightforward, and not too overwhelming 
Response handling.

# Integration
---
Testing the frontend javascript request and then processing what the back end is sending it. Essentially, testing the interaction between the client and the server 
