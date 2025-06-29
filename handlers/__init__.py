from aiogram import Router

from handlers.start import router as start_router
from handlers.adding import router as adding_router

router = Router()

router.include_routers(
    start_router,
    adding_router
)