def product_data():
    return {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


def products_data():
    return [
        {"name": "Iphone 11 Pro Max", "quantity": 20, "price": "4.500", "status": True},
        {"name": "Iphone 12 Pro Max", "quantity": 15, "price": "5.500", "status": True},
        {"name": "Iphone 13 Pro Max", "quantity": 5, "price": "6.500", "status": True},
        {
            "name": "Iphone 15 Pro Max",
            "quantity": 3,
            "price": "10.500",
            "status": False,
        },
    ]


def products_with_price_range():
    """Produtos para testar filtros de preço (5000 < price < 8000)"""
    return [
        {"name": "Samsung Galaxy S21", "quantity": 15, "price": "3.000", "status": True},  # Fora do range
        {"name": "Samsung Galaxy S22", "quantity": 12, "price": "5.500", "status": True},  # Dentro do range
        {"name": "Samsung Galaxy S23", "quantity": 8, "price": "6.500", "status": True},   # Dentro do range
        {"name": "Samsung Galaxy S24", "quantity": 5, "price": "7.500", "status": True},   # Dentro do range
        {"name": "Samsung Galaxy S25", "quantity": 3, "price": "9.000", "status": True},   # Fora do range
    ]
