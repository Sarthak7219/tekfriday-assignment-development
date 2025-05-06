# TekFriday Assignment – Loan Risk Classifier

Here is my submission for the TekFriday Assignment (Development).
- Submitted by: Sarthak Rangari
- Email: sarthakrangari788@gmail.com

This is a FastAPI-based backend application with a simple frontend interface. It performs the following tasks:

1. Answers basic loan-related questions through a chatbot.
2. Calculates individual loan risk scores.
3. Classifies and updates risk levels in a batch Excel dataset.

## Features

- Chatbot API for predefined loan FAQs.
- Risk score calculator using the formula: score = (missed_repayments * 2) + (loan_amount / collateral_value) + (interest / 2)
- Score < 15 → LOW
- 15 ≤ Score ≤ 25 → MEDIUM
- Score > 25 → HIGH

- Batch processing and tagging of risk levels in `dataset.xlsx`.

## How to Run

1. Install dependencies:
   ``` pip install fastapi uvicorn pandas openpyxl```
   
2. Start the server:
   ```uvicorn main:app --reload```

3. Access the frontend at: `http://localhost:8000`

## API Endpoints

- `POST /chat` – Ask loan-related questions.
- `POST /calculate-risk` – Submit data to get a risk level.
- `GET /batch-risk` – Classify and update risk levels in the Excel file.
