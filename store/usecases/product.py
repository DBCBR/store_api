from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut, ProductFilter
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database("test")
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product_model = ProductModel(**body.model_dump())
            await self.collection.insert_one(product_model.model_dump())
            return ProductOut(**product_model.model_dump())
        except Exception as e:
            from store.core.exceptions import InsertionException
            raise InsertionException(
                message=f"Error inserting product: {str(e)}")

    async def get(self, id: UUID) -> ProductOut:
        # Converter UUID para string
        result = await self.collection.find_one({"id": str(id)})

        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self, filters: ProductFilter = None) -> List[ProductOut]:
        """Query products with optional price filters"""
        query_filter = {}

        if filters:
            if filters.min_price is not None or filters.max_price is not None:
                price_filter = {}
                if filters.min_price is not None:
                    # Converter Decimal para float para comparação no MongoDB
                    price_filter["$gte"] = float(filters.min_price)
                if filters.max_price is not None:
                    # Converter Decimal para float para comparação no MongoDB
                    price_filter["$lte"] = float(filters.max_price)
                query_filter["price"] = price_filter

        return [ProductOut(**item) async for item in self.collection.find(query_filter)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        from datetime import datetime, timezone

        # Adicionar updated_at ao body
        update_data = body.model_dump(exclude_none=True)
        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            filter={"id": str(id)},  # Converter UUID para string
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        # Converter UUID para string
        product = await self.collection.find_one({"id": str(id)})
        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: {id}")

        # Converter UUID para string
        result = await self.collection.delete_one({"id": str(id)})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
