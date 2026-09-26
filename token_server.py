import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
from config import config

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/token")
async def get_token(room: str, identity: str):
    """
    Mints a LiveKit access token for a user.
    """
    if not room or not identity:
        raise HTTPException(status_code=400, detail="Room and Identity are required")

    try:
        token = api.AccessToken(config.LIVEKIT_API_KEY, config.LIVEKIT_API_SECRET) \
            .with_identity(identity) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room,
            ))
        return {"token": token.to_jwt()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
