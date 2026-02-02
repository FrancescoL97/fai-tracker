# FAI Tracker

Desktop application to manage FAI documentation and compliance, allowing user to insert, update, verify and expiry tracking of FAI documentation.

## Problem
- FAI documents stored directly in SAP, resulting in time-consuming research
- Difficulty to verify if a FAI already exists for a given Part Number
- Risk of using expired documentation
- Manual checks are time-consuming and error-prone

## Features
- Insert new FAI (PDF, ZIP or folder)
- Automatic renaming and archiving based on PN and issue date 
- Update existing FAI with versioning and archival of expired ones 
- Verify FAI by Part Number 
- Expiry tracking and expired FAI report 
- Separation between active archive and historical archive

## Tech stack
- Python
- Desktop GUI (Qt)
- Local file system
- Local indexing (SQLite)
- Windows environment