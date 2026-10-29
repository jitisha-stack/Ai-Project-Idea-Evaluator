# AI Project Idea Evaluator

A beginner-friendly Streamlit web app that evaluates project feasibility across six pillars and optionally uses an OpenAI API to explain results.

## Features
- Six-pillar weighted score (0–100)
- Financial estimate and simple payback estimate
- Risk and privacy warnings
- Build-vs-buy guidance
- Interactive charts and downloadable text report
- Optional AI explanation
- Unit tests

## Setup
Install Python 3.10 or newer, extract this ZIP, and open this folder in VS Code.

### Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install and run
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed in the terminal, usually `http://localhost:8501`.

## Optional AI explanation
The app works without an API key. To enable the AI layer:
1. Obtain an API key from your OpenAI developer account.
2. Copy `.env.example` to `.env`.
3. Replace `put_your_key_here` with your key.
4. Keep `.env` private; never upload it to GitHub or share it with teammates.
5. Restart Streamlit and turn on **Use AI explanation**.

API usage may incur charges. ChatGPT subscriptions and API billing are separate. Never put an API key in frontend/browser code.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Demo inputs
The app starts with an AI College Attendance Predictor example: ₹50,000 budget, ₹1,20,000 estimated annual benefit, moderate risk and sliders for data/team readiness. Click **Evaluate project** to see the score, charts, risks, recommendation and report download.

## Scoring design
Financial fit 20%; Risk & safety 20%; Team readiness 15%; Data readiness 20%; Build vs buy 10%; Post-launch plan 15%. These are prototype design choices, not validated industry benchmarks.

## Four-person team division
1. Research and requirements: user problem, scoring criteria and evidence.
2. Scoring and finance: weights, risk rules, costs and ROI.
3. UI and integration: Streamlit, charts, API layer and report download.
4. Testing and documentation: tests, screenshots, user guide, presentation and limitations.
