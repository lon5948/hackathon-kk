document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const address = document.getElementById("address").value;

    if (name.trim() !== "" && email.trim() !== "" && address.trim() !== "") {
      localStorage.setItem("name", name);
      localStorage.setItem("email", email);
      localStorage.setItem("address", address);
      window.location.href = "url.html";
    } else {
      alert("Please fill in all fields.");
    }
  });
