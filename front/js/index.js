let products = []
let cart = []
const cartData = JSON.parse(localStorage.getItem("cart"));
let total = 0;
const MY_SERVER = "https://super-django-1.onrender.com/"
const token = sessionStorage.getItem("token") || null
const tokenData = {
  "Content-Type": "application/json",
  "Authorization": "Bearer " + token,
}
// const current_user=parseJwt(token).username || null



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
  }
  displayCartLink()
}

const displayCartLink = () => {
  const yourCartElement = document.getElementById("yourCart");
  if (yourCartElement) {
    if (cart.length === 0 || !cart) {
      yourCartElement.innerHTML = "your cart(0)";
    }
    else yourCartElement.innerHTML = `your cart(${cart.length})`;
  }
};
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
  displayCartLink()
}

// Display order history in the div
const displayOrderHistory = () => {
  axios.get(MY_SERVER + 'history', { headers: tokenData })
    .then((response) => {
      const orderHistory = response.data.orders;
      if (orderHistory.length === 0) {
        showErrorNotification("No history of orders. Lets create new history:)")
        return
      }
      orderHistory.reverse()//to get last one first
      user = parseJwt(token).username || null
      // Build the HTML content for displaying order history
      displayy.innerHTML = ''
      displayy.innerHTML = `
        <h1>your order history, ${user}</h1>
        <ul>
          ${orderHistory.map(order => `
            <li>
              <strong>Order Date:</strong> ${order.order_date}<br>
              <strong>Products:</strong>
              <ul>
                ${order.order_details.map(detail => `
                  <li>
                    Product: ${detail.product_desc}<br>
                    Quantity: ${detail.quantity}
                  </li>
                `).join('')}
              </ul>
            </li>
          `).join('')}
        </ul>
      `;

      // Set the content of the order history div
      orderHistoryDiv.innerHTML = orderHistoryHtml;
    })
    .catch((error) => {
      if (error.response.status === 401) {
        showErrorNotification("Unauthorized. Please log in")
        setTimeout(() => {
          window.location.href = "login.html";
        }, 2000);//take user to login page if unauthorized
      }
      console.error('Error fetching order history:', error);
    });
}