from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import certifi

app = Flask(__name__)

# ==============================
# Подключение к MongoDB
# ==============================
client = MongoClient(
    "mongodb+srv://izimovdaniar10_db_user:050773Ltidd@daniyar.f5v5kq4.mongodb.net/?retryWrites=true&w=majority&appName=daniyar",
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["myshopdb"]
collection = db["inventory"]

# ==============================
# Главная страница
# ==============================
@app.route("/")
def index():
    return render_template("index.html")

# ==============================
# Страница добавления товара
# ==============================
@app.route("/add")
def add_page():
    return render_template("add_item.html")

# ==============================
# Страница со всеми товарами
# ==============================
@app.route("/my_items")
def my_items():
    items = list(collection.find())
    return render_template("my_items.html", items=items)

# ==============================
# Добавление товара
# ==============================
@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form["name"]
    item_type = request.form["type"]
    production = request.form["production"]
    quality = request.form["quality"]
    image = request.form["image"]  # путь к картинке внутри static/photo
    quantity = int(request.form["quantity"])

    collection.insert_one({
        "name": name,
        "type": item_type,
        "production": production,
        "quality": quality,
        "quantity": quantity,
        "image": image
    })
    return redirect("/my_items")

# ==============================
# Удаление товара
# ==============================
@app.route("/delete_item", methods=["POST"])
def delete_item():
    name = request.form["name"]
    collection.delete_one({"name": name})
    return redirect("/my_items")

# ==============================
# Запуск приложения
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
