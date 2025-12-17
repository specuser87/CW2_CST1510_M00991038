# CW2_CST1510_M00991038
Student: Babafemi Ajayi
Module: CST1510 - Coursework 1
Tier: Tier Three (All Three Domains)



Project Overview

The Multi-Domain Intelligence Platform is a web application built on Python and streamlt that serves three user groups:

- Cybersecurity Analysts - Monitor and analyze security incidents

- Data Scientists - Manage datasets and analyze the resource consumption

- IT Admin - Track service desk performance and resolve tickets


# Core Problems Addressed

Cybersecurity Domain

Phishing incidents surges cause a resolution bottleneck.
Solution: Dashboard identifies threat trends and analyzes resolution time by its threat category.



 Data Science Domain

 Dataset resource management and governance
 Solution: Would analyze stroage consumption and provide archiving policy recommendations

  IT Operations Domain

  Slow ticket resolutions and staff perfomance issues.
  Solution: Identification of performance bottlenects and process delays.


# ---------------------------------------------------------------

# Features Implemented

Week 7: Security and Authentication

- Secure password hashing using bcrypt
- User registration and login system
- Role-based access control


Week 8: Database and CRUD Operations

- Four tables: users, cyber_incidents, datasets_metadata and it_tickets
- Full CRUD operations for all domains
- Data migration from text files to database
- CSV data loading with pandas

Week 9: Web Interface & Visualizations

- Multi-page Streamlit application
- Session state management
- Interactive dashboards for all three domains
- Data visualizations using Plotly:

- Pie charts for distribution analysis
- Bar charts for comparisons
- Line charts for trends
- Scatter plots for correlations


- Filtering and search functionality
- Interactive CRUD forms

Week 10: AI Integration

- Google Gemini AI integration
- Context-aware AI assistant for each domain
- Automated trend analysis and recommendations
- Interactive chat interface


Technology Stack

Language: Python 3.x
Framework: Streamlit
Database: SQLite3
Authentication: bcrypt
Data Processing: pandas
Visualization: Plotly
AI: OpenAI API
Environment: python-dotenv


Project Structure
CW2_CST1510_M00991038/
├── DATA/
│   ├── intelligence_platform.db    # SQLite database
│   ├── cyber_incidents.csv         # Sample cybersecurity data
│   ├── datasets_metadata.csv       # Sample dataset data
│   └── it_tickets.csv              # Sample IT ticket data
├── pages/
│   ├── 1_Login.py              # Authentication page
│   ├── 2_Cybersecurity.py     # Cyber incidents dashboard
│   ├── 3_Data_Science.py       # Dataset management dashboard
│   └── 4_IT_Operations.py      # IT tickets dashboard
├── .env                            # Environment variables (API keys)
├── .gitignore                      # Git ignore file
├── ai_assistant.py                 # AI integration module
├── app.py                          # Main Streamlit application
├── database.py                     # Database manager class
├── README.md                       # This file
└── requirements.txt                # Python dependencies

Installation & Setup
1. Clone the Repository
bashgit clone [your-repo-url]
cd CW2_CST1510_M00991038
2. Install Dependencies
bashpip install -r requirements.txt
3. Set Up Environment Variables
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key_here
Get your Gemini API key from: https://aistudio.google.com/app/apikey
4. Initialize the Database
bashpython database.py
This will:

Create all required tables
Migrate users from Week 7 (if available)
Load sample data from CSV files

5. Run the Application
bashstreamlit run app.py
The application will open in your browser at http://localhost:8501

 Default Users
After database initialization, you can:

Login with migrated users from Week 7
Register a new account via the Login page


Key Insights Delivered
Cybersecurity Dashboard

Identifies Phishing as the most common threat type
Shows high-severity unresolved incident backlog
Calculates average resolution time by threat category
AI recommendations for threat mitigation

Data Science Dashboard

Analyzes storage consumption by department
Identifies largest datasets for archiving
Calculates row count vs file size correlation
AI-powered data governance policy recommendations

IT Operations Dashboard

Identifies staff performance bottlenecks
Highlights "Waiting for User" status delays
Tracks resolution time trends
AI analysis of process inefficiencies


Security Features

Password hashing with bcrypt (salt rounds: 12)
SQL injection prevention via parameterized queries
Session-based authentication
Environment variable protection for API keys
.gitignore prevents sensitive data commits


Future Enhancements

Export reports to PDF
Email notifications for high-severity incidents
Advanced analytics with machine learning
Real-time data refresh
Multi-language support
Mobile-responsive design improvements


 License
This project is submitted as coursework for CST1510 at Middlesex University.

 Author
Babafemi Ajayi
Student ID: M00991038
Middlesex University
December 2025

Acknowledgments

Course materials from CST1510
Streamlit documentation
ChatGPT OpenAI API
Plotly visualization library