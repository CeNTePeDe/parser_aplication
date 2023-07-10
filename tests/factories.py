import random

import factory

from models.product_models import CategoryModel, ProductModel


class CategoryFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = CategoryModel

    category = "test_category"


class ProductFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = ProductModel

    name_product = "test_product"
    picture_link = factory.Faker("url")
    price = str(random.uniform(50.0, 500.0))
    product_detail_link = factory.Faker("url")
    characteristic = {}
    description = "description"
    category = factory.SubFactory(CategoryFactory)
    product_id = "product0"
