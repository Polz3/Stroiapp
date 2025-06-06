from app.api.auth import router as auth_router

def init_routes(app):
    app.include_router(auth_router)
