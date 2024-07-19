// Jquery be like
const $ = (selector) => document.querySelector(selector);
const $id = (id) => document.getElementById(id);

function displayLoadingModal() {
  const modal = $(".modal-load");
  modal.style.display = "block";
}

function hideLoadingModal() {
  const modal = $(".modal-load");
  modal.style.display = "none";
}

function displayForm() {
  const general = $("#general");
  general.style.display = "flex";
  const box_atras = $("#box-atras");
  box_atras.style.display = "none";
}

function hideForm() {
  const general = $("#general") === null ? $("#audiogeneral") : $("#general");
  general.style.display = "none";
  const box_atras = $("#box-atras");
  box_atras.style.display = "flex";
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
    "Track id",
    "Track name",
    "Track artist",
    "Lyrics",
    "Track popularity",
    "Track album id",
    "Track album name",
    "Track album release date",
    "Playlist name",
    "Playlist id",
    "Playlist genre",
    "Playlist subgenre",
    "Danceability",
    "Energy",
    "Key",
    "Loudness",
    "Mode",
    "Speechiness",
    "Acousticness",
    "Instrumentalness",
    "Liveness",
    "Valence",
    "Tempo",
    "Duration (ms)",
    "Language",
  ];
  const head = $("thead");
  head.innerHTML = headers.map((header) => `<th>${header}</th>`).join("");
}

// fetch lines from the server and display a row for each one
function fetchLines() {
  const consulta = $id("inp-consulta").value;
  if (!consulta) return; // empty query -> do nothing

  displayLoadingModal();
  const tecnica = $id("inp-tecnica").value;

  fetch(`/api/query/${tecnica}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: consulta,
      topK: $id("inp-topK").value,
      rows: $('input[name="inp-rows"]:checked').value,
    }),
  })
    .then((response) => response.json())
    .then((json) => {
      hideLoadingModal();
      createHeader();
      const tbody = $("tbody");
      json.result.forEach((line) => {
        const tr = document.createElement("tr");
        for (const key in line) {
          const td = document.createElement("td");
          if (key !== "3") {
            td.textContent = line[key];
          } else {
            const buttonLyrics = document.createElement("button");
            buttonLyrics.textContent = "Mostrar letra";
            buttonLyrics.addEventListener("click", () => {
              loadLyrics(line, key);
            });
            td.appendChild(buttonLyrics);
          }
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      });
      hideTipo();
      hideForm();
      const durationTime = $id("duration-time");
      durationTime.textContent = json.time + " ms";
      const sConsulta = $id("s-consulta");
      sConsulta.textContent = consulta;
    });
}

function hideTipo() {
  const tipo = $("#box-sel-ret");
  tipo.style.display = "none";
}

function showTipo() {
  const tipo = $("#box-sel-ret");
  tipo.style.display = "block";
}

function restart() {
  showTipo();
  displayForm();
  // reset table
  const table = $("table");
  table.innerHTML = `
    <thead>
    </thead>
    <tbody>
    </tbody>
  `;
}

function fetchSounds() {
  const audio = $id("audio-consulta").files[0];
  const filename = audio.name;
  if (!audio) return; // empty query -> do nothing

  displayLoadingModal();
  // const tecnica = $id("audio-tecnica").value;
  const modo = $id("audio-modo").value;

  const formData = new FormData();
  formData.append("audio", audio);
  formData.append("filename", filename);

  const routes = {
    secuencial: "/api/audio/knn/lineal",
    rtree: "/api/audio/knn/rtree",
    highD: "api/audio/knn/rtreehighd",
  };
  const fetchRoute = routes[modo];

  fetch(fetchRoute, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((json) => {
      hideLoadingModal();
      const result = json.result;
      const audioList = document.getElementById("audio-list");

      result.forEach((item) => {
        const audioContainer = document.createElement("div");
        audioContainer.classList.add("audio-container");

        const songName = document.createElement("h3");
        songName.textContent = item.name;

        // const audioElement = document.createElement("audio");
        // audioElement.setAttribute("controls", "");
        // audioElement.setAttribute("src", item.url);

        audioContainer.appendChild(songName);
        // audioContainer.appendChild(audioElement);
        audioList.appendChild(audioContainer);
      });
      hideTipo();
      hideForm();
      const durationTime = $id("duration-time");
      durationTime.textContent = json.time + " ms";
      const sConsulta = $id("s-consulta");
      sConsulta.textContent = consulta;
    });
}
