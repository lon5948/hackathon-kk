document.getElementById("urlForm").addEventListener("submit", function (event) {
event.preventDefault();

const url = document.getElementById("url").value;

if (url.trim() !== "") {
    sessionStorage.setItem("url", url);
    window.location.href = "chatroom.html";
} else {
    alert("Please fill in all fields.");
}
});