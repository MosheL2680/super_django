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



// Load cart list from local storage (and call for display)
const loadCart = () => {
  if (cartData != null) {
    cart = cartData
  }
  displayCart()
}

// Display cart
const displayCart = () => {
  if (cart.length === 0 || !cart) {
    changePageError('index.html', 'your cart is empty')
  }
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
    try {
      let response = await axios.post(MY_SERVER + "checkout", { cart: cartData }, { headers: tokenData });//send cart and token to server
      if (response.data === "order saved fucking successfuly") {
        localStorage.removeItem("cart");//delete cart from localstorage
        cart = []//clear cart var
        changePageSuccess('index.html', `chckout successfuly. you need to pay ${total}$`)
      }
    } catch (error) {
      if (error.response.status === 401) {
        changePageError('login.html', 'Unauthorized. Please log in')
      }
      else {

        console.log("Failed to perform the checkout.");
      }
    }
  }
}