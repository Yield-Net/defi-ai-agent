# 🧠 AI-Powered DeFi Strategy Generator 🧠

This is a backend agent that takes a **user's investment profile** and current **DeFi protocol data**, and returns a **Gemini-generated investment strategy** tailored to the user.

Built with:
- FastAPI
- Gemini LLM
- DeFi Llama
- Testnet-ready architecture

---

## Sample User Input JSON

Send this to the `/generate-strategy` endpoint:

```json
{
  "risk_tolerance": "moderate",
  "investment_amount": 1000,
  "investment_currency": "USDC",
  "investment_horizon": "medium",
  "experience_level": "beginner",
  "investment_goals": ["passive_income"],
  "preferred_activities": ["lending", "staking", "liquidity_providing"]
}
```

---

## 📤 Sample LLM Strategy Output JSON

This is what you'll receive back:

```json
{
  "strategy": [
    {
      "protocol": "AAVE V3",
      "activity": "lending",
      "token": "USDC",
      "allocation_percent": 70,
      "expected_apy": 2.5,
      "estimated_return": 17.5,
      "risk_level": "low",
      "why": "AAVE is a well-established lending protocol with stable yield."
    },
    {
      "protocol": "Uniswap V3",
      "activity": "liquidity_providing",
      "token": "ETH/USDC LP",
      "allocation_percent": 30,
      "expected_apy": 4.1,
      "estimated_return": 12.3,
      "risk_level": "moderate",
      "why": "Uniswap offers strong LP returns with manageable risk."
    }
  ]
}
```

---

## 🚀 Running the Project

### 🔧 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your Gemini key:

```env
GEMINI_API_KEY=your-gemini-api-key
```

### ▶️ Start the server

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger API interface.

---

## 📡 Endpoints

| Method | Endpoint              | Description                      |
|--------|-----------------------|----------------------------------|
| GET    | `/market-context`     | Fetch DeFi protocols from Llama |
| POST   | `/user-profile`       | Submit a user profile           |
| POST   | `/generate-strategy`  | Get a tailored strategy (Gemini) |

