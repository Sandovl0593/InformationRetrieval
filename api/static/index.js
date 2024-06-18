// Jquery be like
const $ = (selector) => document.querySelector(selector);

function setupTopK() {
  const topKValue = $("#topK-value");
  const inpTopK = $("#inp-topK");
  inpTopK.addEventListener("input", () => {
    topKValue.innerHTML = inpTopK.value;
  });
}

// fetch lines from the server and display a row for each one
async function fetchLines() {
  // const response = await fetch("/api/query");
  const response = await fetch("/api/csv");
  const lines = await response.json();
  const tbody = $("tbody");
  tbody.innerHTML = "";
  lines.forEach((line) => {
    const tr = document.createElement("tr");
    for (const key in line) {
      const td = document.createElement("td");
      if (key !== "3") {
        td.textContent = line[key];
      } else {
        const buttonLyrics = document.createElement("button");
        buttonLyrics.textContent = "Mostrar letra";
        buttonLyrics.addEventListener("click", () => {
          const modal = $(".modal");
          const title = $("#modal-title");
          const modalText = $("#modal-text");
          modalText.textContent = line[key];
          title.textContent = line[1];
          modal.style.display = "block";
          const span = $(".close");
          span.onclick = function () {
            modal.style.display = "none";
          };
          window.onclick = function (event) {
            if (event.target == modal) {
              modal.style.display = "none";
            }
          };
        });
        td.appendChild(buttonLyrics);
      }
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  });
}


setupTopK();