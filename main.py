from routes import user_router,product_router, category_router, order_router, order_item_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="E-Commerce API", version="1.0.0")


@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(user_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(order_item_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)