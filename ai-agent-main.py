import json
import re
import requests
from typing import Union
import google.generativeai as genai
from dotenv import load_dotenv
from models import UserProfile, RiskTolerance, InvestmentHorizon, ExperienceLevel, InvestmentGoal, DeFiActivity

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Helper: Detect if the message implies profile changes and generate updated profile
def analyse_user_message(user_profile: dict, user_message: str) -> dict:
    prompt = f"""
You are a DeFi portfolio assistant.

The user has sent this message: "{user_message}"

Here is their current investment profile:
{json.dumps(user_profile, indent=2)}

You must do the following:

1. Determine if the message indicates a change to the user's investment profile.
2. If yes, update the profile accordingly and return the new profile.
3. If no, return a friendly, short response to the message without changing anything.

Respond ONLY with a JSON object of the following format:
{{
  "profile_changed": true/false,
  "updated_profile": {{...}}, // Only if changed
  "response": "Your response to the user" 
}}

ONLY return valid JSON, and do not include commentary or extra messages.
Ensure enum values exactly match the following:

- risk_tolerance: conservative, moderately_conservative, moderate, moderately_aggressive, aggressive
- investment_horizon: short, medium, long
- experience_level: beginner, intermediate, advanced
- investment_goals: passive_income, capital_growth, wealth_preservation, portfolio_diversification
- preferred_activities: staking, yield_farming, lending, liquidity_providing, trading
"""
    response = model.generate_content(prompt)
    try:
        content = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(content)
    except Exception as e:
        return {"profile_changed": False, "response": "Sorry, I couldn’t understand that. Could you rephrase?"}

# Helper: Generate strategy from updated profile
def get_strategy_from_api(updated_profile: dict) -> Union[list, dict]:
    try:
        res = requests.post(
            url="http://yourapi.com/strategies/generate-strategy",
            json=updated_profile,
            timeout=10
        )
        res.raise_for_status()
        
        # here update teh database
        
        
        return res.json()
    except Exception as e:
        return {"error": "Failed to fetch strategy", "details": str(e)}

# Main service function
def handle_user_message(user_profile: UserProfile, user_message: str) -> dict:
    profile_dict = json.loads(user_profile.json())
    analysis = analyse_user_message(profile_dict, user_message)

    if analysis.get("profile_changed"):
        updated_profile = analysis["updated_profile"]
        strategy = get_strategy_from_api(updated_profile)
        return {
            "message": analysis["response"],
            "profile_changed": True,
            "updated_profile": updated_profile,
            "new_strategy": strategy
        }
    else:
        return {
            "message": analysis["response"],
            "profile_changed": False
        }
