import redis
from django.conf import settings
from shop.models import Product
import os
# соединить с redis
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/1")

# Создаём Redis клиент из URL
r = redis.from_url(redis_url)


class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # получить другие товары, купленные
                # вместе с каждым товаром
                if product_id != with_id:
                    # увеличить балл товара,
                    # купленного вместе
                    r.zincrby(self.get_product_key(product_id),
                              1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # только 1 товар
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # сгенерировать временный ключ
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # несколько товаров, объединить баллы всех товаров
            # сохранить полученное сортированное множество
            # во временном ключе
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # удалить идентификаторы товаров,
            # для которых дается рекомендация
            r.zrem(tmp_key, *product_ids)
            # получить идентификаторы товаров по их количеству,
            # сортировка по убыванию
            # удалить временный ключ
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # получить предлагаемые товары и
        # отсортировать их по порядку их появления
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
