# Restaurant Feedback System

A web-based restaurant feedback system that enables customers to submit feedback while providing an interactive dashboard for feedback analysis.

## Features
- Customer feedback submission with input validation (Egyptian mobile numbers)
- Search a customer's feedback by phone number
- Edit or delete a single feedback record (with delete confirmation)
- Interactive analytics dashboard
- Export all feedback to Excel
- Data stored in an Excel file (`feedback.xlsx`, created automatically on first run)

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL

## Project Structure
- `app.py` – main page: feedback form, search, edit, delete and export
- `database.py` – reading, writing and validating data in the Excel file
- `dashboard.py` – KPIs and charts

## How to Run

1. Install the required libraries:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python -m streamlit run app.py
```

## Screenshots

### Dashboard
![Dashboard](dashboard.jpg)

### Dashboard (Analysis)
![Dashboard 2](dashboard2.jpg)

### Feedback Form
![Feedback Form](feedback_form.jpg)

## Author
Karim Reda
