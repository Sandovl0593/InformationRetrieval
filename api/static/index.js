// Jquery be like
const $ = (selector) => document.querySelector(selector);
const $id = (id) => document.getElementById(id);

function displayLoadingModal() {
  const modal = $(".modal-load");
  // setTimeout(() => {
  //   modal.style.display = "block";
  // }, 1000);
  modal.style.display = "block";
}

function hideLoadingModal() {
  const modal = $(".modal-load");
  modal.style.display = "none";
}

function loadLyrics(line, key) {
  const modal = $(".modal");
  const title = $("#modal-title");
  const modalText = $("#modal-text");
  modalText.textContent = line[key];
  title.textContent = line[1];
  modal.style.display = "block";
  const span = $(".close");
  span.onclick = () => {
    modal.style.display = "none";
  };
  window.onclick = (event) => {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
}

function createHeader() {
  const headers = [
    "Track id","Track name","Track artist","Lyrics","Track popularity",
    "Track album id","Track album name","Track album release date","Playlist name",
    "Playlist id","Playlist genre","Playlist subgenre","Danceability","Energy","Key",
    "Loudness","Mode","Speechiness","Acousticness","Instrumentalness","Liveness",
    "Valence","Tempo","Duration (ms)","Language"
  ];  
  const head = $("thead");
  head.innerHTML = headers.map(header => `<th>${header}</th>`).join('');
}

// fetch lines from the server and display a row for each one
function fetchLines() {
  displayLoadingModal();
  const consulta = $id("inp-consulta").value;
  const tecnica = $id("inp-tecnica").value;
  fetch(`/api/query/${tecnica}`, {
    method: "POST", headers: { "Content-Type": "application/json",},
    body: JSON.stringify({
      query: consulta,
      topK: $id("inp-topK").value,
    }),
  })
  .then((response) => response.json())
  .then(json => {
    hideLoadingModal();
    const tbody = $("tbody");
    createHeader();
    json.forEach((line) => {
      const tr = document.createElement("tr");
      for (const key in line.result) {
        const td = document.createElement("td");
        if (key !== "3") {
          td.textContent = line[key];
        } else {
          const buttonLyrics = document.createElement("button");
          buttonLyrics.textContent = "Mostrar letra";
          buttonLyrics.addEventListener("click", () => {loadLyrics(line, key); });
          td.appendChild(buttonLyrics);
        }
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    });
  })
}