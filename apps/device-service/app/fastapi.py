from typing import Callable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.device import DeviceRouter

def router(app: FastAPI) -> FastAPI:
	app.include_router(DeviceRouter)
	return app

def middleware(app: FastAPI) -> FastAPI:
	app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'], allow_methods=['GET', 'POST'], allow_credentials=False)
	return app

def construct(lifespan: Callable = None) -> FastAPI:
	app = FastAPI() if lifespan is None else FastAPI(lifespan=lifespan)
	app = middleware(app)
	app = router(app)
	return app
