from aiogram import Router

from handlers.start import router as start_router

router = Router()

router.include_routers(
    start_router
)