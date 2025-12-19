from fastapi import HTTPException

class InventoryService:
	def __init__(self, product_repo):
		self.product_repo = product_repo

	async def validate_products_and_quantities(self, items):
		"""
		Validates all products exist and have sufficient stock.
		Returns dict of product_id:product for further use.
		Raises HTTPException if any product is invalid or stock is insufficient.
		"""
		products = {}
		for item in items:
			product = await self.product_repo.get_by_id(item.product_id)
			if not product:
				raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
			if product.stock < item.quantity:
				raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
			products[item.product_id] = product
		return products

	async def reduce_stock(self, items, session, products=None):
		"""
		Reduces stock for all products in items. Assumes validation already done.
		Accepts optional products dict to avoid re-fetching.
		Returns dict of product_id:product for further use.
		"""
		if products is None:
			products = await self.validate_products_and_quantities(items)
		for item in items:
			product = products[item.product_id]
			product.stock -= item.quantity
			session.add(product)
		return products

	async def low_stock_alerts(self, threshold=5):
		"""
		Returns a list of products with stock below the given threshold.
		"""
		# Assumes product_repo has a method to get all products
		products = await self.product_repo.get_all()
		low_stock_products = [p for p in products if p.stock < threshold]
		return f"Low stock products: {[p.id for p in low_stock_products]}"
