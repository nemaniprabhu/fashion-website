from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "shopping_secret_key_123"   # ⭐ secret key here

# Fake database (temporary users storage)
users = {}

# ---------------- HOME PAGE ----------------
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists!"

        users[username] = password
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- CART PAGE ----------------
@app.route("/add_to_cart/<item>")
def add_to_cart(item):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(item)
    session.modified = True
    return redirect("/cart")

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart=cart_items)



# ---------------- CATEGORY PAGES ----------------
@app.route("/men")
def men():
    return render_template("men.html")

@app.route("/women")
def women():
    return render_template("women.html")

@app.route("/kids")
def kids():
    return render_template("kids.html")

@app.route("/traditional")
def traditional():
    return render_template("traditional.html")

@app.route("/tshirts")
def tshirts():
    return render_template("tshirts.html")

# ---------------- ACCOUNT PAGE ----------------
@app.route("/account")
def account():
    username = session.get("user", "Guest")
    cart_items = session.get("cart", [])

    return render_template(
        "account.html",
        username=username,
        cart_count=len(cart_items))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_items = session.get("cart", [])

    if request.method == "POST":
        session["cart"] = []
        return redirect("/order_success")

    return render_template("checkout.html", cart=cart_items)


@app.route("/order_success")
def order_success():
    return render_template("order_success.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()

    products = [
        {"name": "Denim Jacket", "price": "₹1499", "page": "/men"},
        {"name": "Casual T-Shirt", "price": "₹599", "page": "/men"},
        {"name": "Women Dress", "price": "₹999", "page": "/women"},
        {"name": "Kids Hoodie", "price": "₹699", "page": "/kids"},
        {"name": "Formal Shirt", "price": "₹899", "page": "/men"},
        {"name": "Party Gown", "price": "₹1999", "page": "/women"},
    ]

    results = []

    for product in products:
        if query in product["name"].lower():
            results.append(product)

    return render_template("search.html", results=results, query=query)

@app.route("/add_wishlist/<item>")
def add_wishlist(item):
    if "wishlist" not in session:
        session["wishlist"] = []

    if item not in session["wishlist"]:
        session["wishlist"].append(item)

    session.modified = True
    return redirect("/wishlist")


@app.route("/wishlist")
def wishlist():
    wishlist_items = session.get("wishlist", [])
    return render_template("wishlist.html", wishlist=wishlist_items)


@app.route("/remove_wishlist/<item>")
def remove_wishlist(item):
    wishlist_items = session.get("wishlist", [])

    if item in wishlist_items:
        wishlist_items.remove(item)
        session["wishlist"] = wishlist_items
        session.modified = True

    return redirect("/wishlist")

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
    