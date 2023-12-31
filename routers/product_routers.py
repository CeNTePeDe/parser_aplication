import json
import logging
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AnyUrl

from database import CategoryDAO, ProductDAO
from kafka_producers.kafka_products import (
    consumer_products,
    send_data_to_kafka_products,
)
from models.product_models import CategoryModel, ProductModel

logger = logging.getLogger(__name__)

product_routers = APIRouter()


@product_routers.post(
    "/parser", status_code=status.HTTP_201_CREATED, response_model=ProductModel
)
def post_products(
    url: AnyUrl,
    product_dao=Depends(ProductDAO),
    category_dao=Depends(CategoryDAO),
) -> dict:
    logger.info("get url")

    send_data_to_kafka_products(url)
    logger.info("retrieve data from kafka")
    category = CategoryModel(category=url.split("/")[-2])

    for product in consumer_products:
        product = json.loads(product.value)
        logger.info(f"product {type(product)}")
        product_id = product["product_detail_link"].split("/")[-3]
        price = product.pop("price")
        price = Decimal(price)
        category_item = category_dao.create_item(category)
        product = product_dao.create_item(
            ProductModel(
                **product, price=price, category=category_item, product_id=product_id
            )
        )
        logger.info(f"product is {product}")
    return {"message": "products are created"}


@product_routers.get("/", status_code=status.HTTP_200_OK)
async def get_products(
    product_dao=Depends(ProductDAO),
) -> list[ProductModel]:
    return product_dao.get_all_items()


@product_routers.get("/{category_name}", status_code=status.HTTP_200_OK)
async def get_products_by_category(
    category_name,
    product_dao=Depends(ProductDAO),
) -> Optional[list[ProductModel]]:
    return product_dao.get_items_by_category(category_name=category_name)


@product_routers.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(
    product_id: str,
    product_dao=Depends(ProductDAO),
) -> ProductModel:
    product = product_dao.get_item(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductModel,
    product_dao=Depends(ProductDAO),
    category_dao=Depends(CategoryDAO),
) -> ProductModel:
    logger.info("product create is started")
    category = product.category
    category_dao.create_item(category)
    product = product_dao.create_item(product)
    logger.info("product is created")
    return product


@product_routers.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str,
    product: ProductModel,
    product_dao=Depends(ProductDAO),
) -> ProductModel:
    new_product = product_dao.update_item(product_id, product)
    if new_product == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return new_product


@product_routers.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    product_dao=Depends(ProductDAO),
) -> None:
    if product_dao.delete_item(product_id) == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info("product is deleted")
