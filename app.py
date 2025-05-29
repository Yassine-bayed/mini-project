from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'ta_cle_secrete_pour_flash'  # nécessaire pour flash messages

mongo = PyMongo(app)

# Folder to save uploaded images
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    category_filter = request.args.get('category')
    sort_order = request.args.get('sort')

    if not category_filter:
        category_filter = 'all'
    if sort_order not in ('asc', 'desc'):
        sort_order = 'asc'

    query = {}
    if category_filter != "all":
        query["category.name"] = category_filter

    sort = [("price", 1)] if sort_order == "asc" else [("price", -1)]

    products = list(mongo.db.products.find(query).sort(sort))
    categories = list(mongo.db.categories.find())

    return render_template('index.html',
                           products=products,
                           categories=categories,
                           selected_category=category_filter,
                           sort_order=sort_order)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    categories = list(mongo.db.categories.find())

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category')

        # Handle file upload
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'images/{filename}'
        else:
            # Use default image if no valid file uploaded
            image_path = 'images/notfound.png'

        # Validate required fields
        if not (name and description and price and stock and category_id):
            flash('Veuillez remplir tous les champs obligatoires', 'danger')
            return render_template('add_product.html', categories=categories)

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash('Prix doit être un nombre et stock un entier', 'danger')
            return render_template('add_product.html', categories=categories)

        category_doc = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        if not category_doc:
            flash('Catégorie invalide', 'danger')
            return render_template('add_product.html', categories=categories)

        new_product = {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "category": {
                "id": category_doc["_id"],
                "name": category_doc["name"]
            },
            "image": image_path,
            "date_added": datetime.utcnow()
        }

        mongo.db.products.insert_one(new_product)
        flash('Produit ajouté avec succès', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html', categories=categories)


if __name__ == '__main__':
    app.run(debug=True)
