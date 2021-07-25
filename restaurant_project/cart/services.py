def check_quantity(product, quantity):
    """Функция проверяет, что количество в корзину не будет добавлено товара
    больше чем есть в наличии"""
    if product.quantity < quantity:
        raise ValueError('Товара меньше, чем хотят добавить')
