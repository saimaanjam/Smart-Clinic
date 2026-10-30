Smart-Clinic
Smart appointment and queue management system

Overview
An academic web-based healthcare prototype enabling registered patients to book, view and cancel appointments with doctors, nurses and midwives.

Project context
Developed to address appointment booking difficulties identified through user feedback, supporting UN Sustainable Development Goal 3.

Technologies
    •	Frontend: HTML, CSS, JavaScript
    •	Backend: Python flask
    •	Database: MySQL

Features
Patient login, appointment booking and cancellation, my appointments, responsive layouts and supporting website pages.

How to run the project
    1. Download the project
    Clone the GitHub repository or download it as a zip file.
    2. Set up the database:
        a. Open my SQL workbench and execute anjam_project_smart_clinic.sql to create the required tables.
        b. Execute project-data-insert-scripts.sql to populate the tables with hypothetical sample data for testing.
        c. Ensure the database schema name matches the one specified in db.py.
    3. Configure database credentials
    Configure your local MI SQL connection details using environment variables. Database passwords are not included in the repository for security reasons.
    4. Install Python dependencies
    Create and activate a Python virtual environment, then install the projects dependencies.
    5. Start the flask backend
    Run the flask application using the appropriate command for the backend configuration.
    6. Open the frontend
    Open the website using VS code live server, ensuring the Flask backend and my SQL Server are running.

Current limitations
Patient registration is frontend only. Automated queue-time calculations are reserved for future development if required.

Future development
Administer assisted registration, and administrator dashboard and further usability improvements.

Security
Database credentials and sensitive information are excluded from this repository. The project uses fictional patient records and is intended for academic demonstration only.

Licence
Smart-Clinic was developed as an academic project for educational and demonstration purposes only. 
All rights reserved. No permission is granted to copy, modify, distribute or use this project commercially without prior written permission from the copyright holder.
