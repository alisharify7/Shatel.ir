from flask import Blueprint


product = Blueprint(
    name="product",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="PublicProductStatic",
)



from . import model
from . import views
