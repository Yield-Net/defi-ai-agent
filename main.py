from fastapi import FastAPI
from models import UserProfile
from market_data import get_filtered_protocols

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
