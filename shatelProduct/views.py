from flask import render_template
from . import product


@product.route("/<string:product_key>/")
def get_product(product_key: str) -> str:
    return render_template("product/product.html")



