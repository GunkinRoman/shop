from fastapi import FastAPI
from auth.auth import router
from products.product import router as product_router
from cart.routers import router as cart_router
from order.routers import router as order_router
from role.routers import router as role_router

def get_app() -> FastAPI:
    app = FastAPI(title="Shop")

    app.include_router(router)
    app.include_router(product_router)
    app.include_router(cart_router)
    app.include_router(order_router)
    app.include_router(role_router)
    # app._pg_pool
    return app 

app = get_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)