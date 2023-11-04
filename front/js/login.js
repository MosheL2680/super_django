//Login - get token from server
const login = async () => {
  const username = uName.value.trim();
  const password = pass.value.trim();

  if (!username || !password) {
    showErrorNotification("Please enter both a username and a password.");
    return;//exit function if input fields are empty
  }

  const loginData = {
    username: username,
    password: password,
  };

  axios.post("http://127.0.0.1:8000/login/", loginData)//send username & pass to server
    .then((response) => {
      const token = response.data.access;
      sessionStorage.setItem('token', token);//save access token to sessionstorage
      showSuccessNotification("You are logged in now");
      setTimeout(() => {
        window.location.href = "index.html";
      }, 2000);//take user back to the shop
    })
    .catch((error) => {
      showErrorNotification("Username or password isn't correct");//tostify if server dosn't recognize user
    });
};


//Register - create new user
const register = async () => {
  const username = uName.value.trim();
  const password = pass.value.trim();

  if (!username || !password) {
    showErrorNotification("Please enter both a username and a password.");
    return;//exit function if input fields are empty
  }

  const registerData = {
    "username": username,
    "password": password,
  };

  try {
    await axios.post("http://127.0.0.1:8000/register", registerData);//send username & pass to server
    showSuccessNotification("User created successfully");
  } catch (error) {
    if (error.response && error.response.status === 500) {
      showErrorNotification("Username is already in use. Please choose another.");//tostify user when server dosn't accept the username
    } else {
      console.error("Registration failed:", error);
    }
  }
};
