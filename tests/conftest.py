import pytest
import asyncio
import httpx
import mongomock_motor

from uuid import UUID
from store.schemas.product import ProductIn, ProductUpdate
from tests.factories import product_data, products_data
from httpx import AsyncClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client():
    # Use mongomock for testing instead of real MongoDB
    return mongomock_motor.AsyncMongoMockClient()


@pytest.fixture
async def product_usecase(mongo_client):
    from store.usecases.product import ProductUsecase
    
    # Create a new instance with the mock client
    usecase = ProductUsecase()
    usecase.client = mongo_client
    usecase.database = mongo_client.get_database("test")
    usecase.collection = usecase.database.get_collection("products")
    
    return usecase


@pytest.fixture
async def test_client():
    """Create an async test client"""
    from store.main import app
    
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver"
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    
    # Clear all collections after each test
    database = mongo_client.get_database("test")
    try:
        collection_names = await database.list_collection_names()
        for collection_name in collection_names:
            if collection_name.startswith("system"):
                continue
            await database[collection_name].delete_many({})
    except Exception:
        # In case of mongomock limitations
        pass


@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
async def product_inserted(product_in, product_usecase):
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in, product_usecase):
    return [await product_usecase.create(body=product_in) for product_in in products_in]
