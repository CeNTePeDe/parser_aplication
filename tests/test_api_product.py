import logging

from core.constant_variables import URL_PRODUCTS
from tests.factories import CategoryFactory, ProductFactory

logger = logging.getLogger(__name__)


def test_get_products(client):
    response = client.get(URL_PRODUCTS)

    assert response.status_code == 200


def test_create_product(client, mongo_mock):
    data = ProductFactory.build()
    category = CategoryFactory.build()
    data_category = {"category": category.category}
    payload = {
        "name_product": data.name_product,
        "picture_link": data.picture_link,
        "price": str(data.price),
        "product_detail_link": data.product_detail_link,
        "characteristic": data.characteristic,
        "description": data.description,
        "category": data_category,
        "product_id": data.product_id,
    }
    logger.info(f"payload is {payload}")

    response = client.post(url=URL_PRODUCTS, json=payload)

    assert response.status_code == 201


def test_get_product(client, mongo_mock):
    product_id = "product0"

    response = client.get(url=URL_PRODUCTS + f"{product_id}")

    assert response.status_code == 200


def test_get_invalid_product(client, mongo_mock):
    product_id = "invalid_product"

    response = client.get(url=URL_PRODUCTS + f"{product_id}")

    assert response.status_code == 404


def test_update_product(client, mongo_mock):
    product_id = "product0"
    data = ProductFactory.build()
    category = CategoryFactory.build()
    data_category = {"category": category.category}
    payload = {
        "name_product": data.name_product,
        "picture_link": data.picture_link,
        "price": 123.7,
        "product_detail_link": data.product_detail_link,
        "characteristic": data.characteristic,
        "description": data.description,
        "category": data_category,
        "product_id": data.product_id,
    }
    logger.info(f"payload is {payload}")

    response = client.put(url=URL_PRODUCTS + f"{product_id}", json=payload)

    assert response.status_code == 200


def test_delete_product(client, mongo_mock):
    product_id = "product0"

    response = client.delete(url=URL_PRODUCTS + f"{product_id}")

    assert response.status_code == 204