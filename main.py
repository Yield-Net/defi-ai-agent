from fastapi import FastAPI
from models import UserProfile
from market_data import get_filtered_protocols
from strategy_gen import generate_strategy

app = FastAPI()

@app.post("/user-profile")
def receive_user_profile(profile: UserProfile):
    return {"message": "User profile received", "data": profile}

@app.get("/market-context")
def get_market_context():
    try:
        data = get_filtered_protocols()
        return {"protocols": data}
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate-strategy")
def generate(profile: UserProfile):
    try:
        # Pass preferred activities to market context
        preferred = [a.value for a in profile.preferred_activities]
        market_data = get_filtered_protocols(preferred)
        strategy = generate_strategy(profile.dict(), market_data)
        return {"strategy": strategy}
    except Exception as e:
        return {"error": str(e)}

