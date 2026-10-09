/* ======================
   MEMORY PATH
====================== */

const isRecordsPage =
  window.location.pathname.includes(
    "/records/"
  );

const isRehearsalPage =
  window.location.pathname.includes(
    "/rehearsal/"
  );

let memoryPath = "/shared/memory.html";

/* rehearsal配下だけ階層調整 */

if (isRecordsPage) {

  memoryPath =
    isRehearsalPage
      ? "../../shared/memory.html"
      : "../shared/memory.html";

}

/* ======================
   MEMORY LOAD
====================== */

fetch(memoryPath + "?v=39", {
  cache: "no-store"
})

  .then(response => response.text())

  .then(data => {

    const container =
      document.getElementById(
        "memory-container"
      );

    if (!container) return;

    container.innerHTML = data;

    /* ======================
       MEMORY SAVE
    ====================== */

    const currentMemory =
      document.body.dataset.memory;

    if (currentMemory) {

      localStorage.setItem(
        "memory" + currentMemory,
        "open"
      );

    }

    /* ======================
       MEMORY TOGGLE
    ====================== */

    const memoryToggle =
      document.querySelector(
        ".memory-toggle"
      );

    const memoryContent =
      document.querySelector(
        ".memory-content"
      );

    if (memoryToggle && memoryContent) {

      memoryToggle.addEventListener(
        "click",
        () => {

          memoryContent.classList.toggle(
            "open"
          );

        }
      );

    }

    /* ======================
       MEMORY UNLOCK
    ====================== */

    const memoryItems =
      document.querySelectorAll(
        ".memory-item"
      );

    memoryItems.forEach(item => {

      const memoryId =
        item.dataset.memory;

      const memoryTitle =
        item.dataset.title;

      let memoryLink =
        item.dataset.link;

      const unlocked =
        localStorage.getItem(
          "memory" + memoryId
        );

      if (unlocked) {

        item.classList.add(
          "memory-open"
        );

        item.innerHTML =

          '<span class="memory-number">' +
          memoryId +
          '</span>' +

          '<a href="' +
          memoryLink +
          '">' +
          memoryTitle +
          '</a>';

      }

      else {

        item.classList.add(
          "memory-locked"
        );

        item.innerHTML =

          '<span class="memory-number">' +
          memoryId +
          '</span>' +

          '<span class="memory-locked-text">' +
          '????' +
          '</span>';

      }

    });

  })

  .catch(error => {

    console.error(
      "memory load error:",
      error
    );

  });
