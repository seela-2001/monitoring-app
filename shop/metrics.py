from prometheus_client import Counter

# Custom business metric
ITEMS_CREATED = Counter("shop_items_created_total", "Total items created")
