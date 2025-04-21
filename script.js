const socket = new WebSocket("ws://localhost:8080");

function sendRequest() {
  const song = document.getElementById("song-request").value;
  if (!song) {
    alert("Please enter a song title or artist!");
    return;
  }

  fetch("/api/request", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query: song })
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        alert("Song requested: " + data.title);
      }
    });
}

socket.onopen = function () {
  console.log("Connected to WebSocket server.");
};

socket.onmessage = function (event) {
  const message = event.data;
  console.log("Received message: " + message);
  const playlist = document.getElementById("playlist");
  const li = document.createElement("li");
  li.textContent = message;
  playlist.appendChild(li);
};
