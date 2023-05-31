from fastapi import FastAPI
from api_user import router as user_router
from api_url import router as url_router
from api_scanned_history import router as url_history
from api_blacklist import router as blacklist_router
from api_scan import router as scan_router
from prediction import makeTokens
import uvicorn

app = FastAPI()

app.include_router(user_router, prefix= "/users")
app.include_router(url_router, prefix= "/urls")
app.include_router(url_history, prefix= "/history")
app.include_router(blacklist_router, prefix= "/black-list")
app.include_router(scan_router, prefix= "/scan")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
