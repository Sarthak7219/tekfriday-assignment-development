from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import os
from fastapi.responses import FileResponse

app = FastAPI()

# Allow CORS for local/dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# --- Part A: Chatbot ---
faq = {
    "what is emi?": "EMI stands for Equated Monthly Installment, the fixed payment made every month.",
    "what is tenure?": "Tenure refers to the duration for which the loan is taken.",
    "what is interest?": "Interest is the cost of borrowing the principal loan amount."
}

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    answer = faq.get(req.question.lower(), "Sorry, I don't understand that question.")
    return {"answer": answer}

# --- Part B: Single Risk Calculator ---
class RiskInput(BaseModel):
    missed_repayments: float
    loan_amount: float
    collateral_value: float
    interest: float

@app.post("/calculate-risk")
def calculate_risk(data: RiskInput):
    score = (data.missed_repayments * 2)
    score += (data.loan_amount / data.collateral_value)
    score += (data.interest / 2)
    if score < 15:
        level = "LOW"
    elif score <= 25:
        level = "MEDIUM"
    else:
        level = "HIGH"
    return {"score": round(score, 2), "risk_level": level}

# --- Part C: Batch Upload & Tagging ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "dataset.xlsx")
_df = pd.read_excel(DATA_PATH, sheet_name="main_loan_base")

# Classification logic
def classify_risk(row):
    score = (row['missed_repayments'] * 2)
    score += (row['loan_amount'] / row['collateral_value'])
    score += (row['interest'] / 2)
    if score < 15:
        return "LOW"
    elif score <= 25:
        return "MEDIUM"
    else:
        return "HIGH"

# Precompute risk levels
_df['risk_level'] = _df.apply(classify_risk, axis=1)

@app.get("/batch-risk")
def get_batch_risk():
    # Recompute risk level (optional, but good for consistency)
    _df['risk_level'] = _df.apply(classify_risk, axis=1)

    # Write updated data back to the Excel file
    with pd.ExcelWriter(DATA_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        _df.to_excel(writer, sheet_name="main_loan_base", index=False)

    return {"message": "Risk levels tagged and written to Excel successfully."}
