let products = []
let cart = []
const cartData = JSON.parse(localStorage.getItem("cart"));
let total = 0;
const MY_SERVER = "http://127.0.0.1:8000/"


// Load products from server (and call for display)
const loadProducts = async () => {
  const res = await axios.get(MY_SERVER + "products")
  products = res.data
  displayProducts()
}

// Display products
const displayProducts = async () => {
  displayy.innerHTML =
    displayy.innerHTML = `<div class="row row-cols-1 row-cols-md-6 g-1">` + products.map((prod, ind) => `
                <div class="col">
                  <div class="card text-bg-dark mb-3">
                    <img src="../static${prod.img}" class="card-img card-img-top" alt="...">
                    <div class="card-body">
                      <h5 class="card-title">${prod.desc}</h5>
                      <p class="card-text">price: ${prod.price}$</p>
                      amount:<input type="number" id="amount_${ind}" value="1">
                      <button onclick="buy(${ind})" class="btn btn-primary btn-sm">Add to cart</button>
                    </div>
                  </div>
                </div>`)
}

// Load cart list from local storage (and call for display)
const loadCart = () => {
  if (cartData != null) {
    cart = cartData
    displayCart()
  }
}

// Display cart
const displayCart = () => {
  total = 0;
  cartDisplay.innerHTML = `<div class="row row-cols-1 row-cols-md-6 g-4">` + cart.map((item, ind) => {
    total += parseInt(item.price) * parseInt(item.amount);//calc total price
    return `
      <div class="col">
        <div class="card text-bg-secondary mb-1"  >
          <img src="../static${item.img}" class="card-img card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">${item.desc} ${item.price}$</h5>
            <p class="card-text">amount: ${item.amount}</p>
            <button onclick="remove(${item.id})">Remove</button>
          </div>
        </div>
      </div>`;
  });
  totalPrice.innerHTML = `<br><h5>Total price: ${total}$</h5>`;//display total outside loop
}

// Add item to cart and save cart in localstorage
const buy = async (ind) => {
  const product = products[ind]
  const quantity = parseInt(document.getElementById(`amount_${ind}`).value) || 1;
  if (quantity <= 0) {
    showErrorNotification("Please enter a valid positive quantity.");
    return;//exit function if user trying to add negativ amount
  }
  if (cart.filter(prd => prd.id === product.id).length > 0) {
    currentProduct = cart.filter(item => item.id === product.id)[0]
    currentProduct.amount = parseInt(currentProduct.amount) + quantity//if item allready exist in cart, just update amount
  }
  else cart.push({ id: product.id, desc: product.desc, price: product.price, img: product.img, category: product.category, amount: quantity })

  localStorage.setItem("cart", JSON.stringify(cart))//save cart to localstorage
  showSuccessNotification("Item added to cart")
  displayCart()
}

// Remove item from cart list
const remove = (id) => {
  cart = cart.filter(item => item.id !== id);//gives a new cart without this item
  localStorage.setItem("cart", JSON.stringify(cart));//save updated cart to localstorage
  showErrorNotification("Itam removed from cart")
  displayCart()
}

// checkout - Send cart to server
const checkOut = async () => {
  if (cart.length === 0) {
    showErrorNotification("Your cart is empty. Add items before checking out.");
    return;//exit function if cart is empty
  }
  const userConfirmed = confirm("Are you sure you want to check out?");//ask user to confirm checkout
  if (userConfirmed) {
    const token = sessionStorage.getItem("token");//get token from sessionstorage
    const headersData = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token,
    }
    try {
      let response = await axios.post(MY_SERVER + "checkout", { cart: cartData }, { headers: headersData });//send cart and token to server
      if (response.data === "order saved fucking successfuly") {
        localStorage.removeItem("cart");//delete cart from localstorage
        cart = []//clear cart var
        showSuccessNotification(`chckout successfuly. you need to pay ${total}$`)
      }
    } catch (error) {
      if (error.response.status === 401) {
        showErrorNotification("Unauthorized. Please log in")
        setTimeout(() => {
          window.location.href = "login.html";
        }, 2000);//take user to login page if unauthorized
      }
      else console.log("Failed to perform the checkout.");
    }
  }
}