const isRehearsalSearchPage =
  window.location.pathname.includes(
    "/rehearsal/"
  );

const pathPrefix =
  isRehearsalSearchPage
    ? "../"
    : "";

/* ======================
   MOBILE MENU
====================== */

const menuToggle =
  document.getElementById(
    "menuToggle"
  );

const globalNav =
  document.getElementById(
    "globalNav"
  );

if (menuToggle && globalNav) {

  menuToggle.addEventListener(
    "click",
    () => {

      globalNav.classList.toggle(
        "open"
      );

    }
  );

}

/* ======================
   ENDING SYSTEM
====================== */

const endingSection =
  document.getElementById(
    "endingSection"
  );

const overlay =
  document.getElementById(
    "endingOverlay"
  );

const buttons =
  document.querySelectorAll(
    ".ending-button"
  );

if (endingSection) {

  window.addEventListener(
    "scroll",
    () => {

      const scrollTop =
        window.scrollY;

      const docHeight =
        document.body.scrollHeight
        - window.innerHeight;

      const progress =
        scrollTop / docHeight;

      const darkness =
        Math.min(
          Math.max(
            (progress - 0.78) * 4.5,
            0
          ),
          0.92
        );

      document.documentElement.style.setProperty(
        "--ending-darkness",
        darkness
      );

      if (progress > 0.82) {

        endingSection.classList.add(
          "visible"
        );

      }

    }
  );

  buttons.forEach(button => {

    button.addEventListener(
      "click",
      () => {

        const link =
          button.dataset.link;

        if (overlay) {

          overlay.classList.add(
            "active"
          );

        }

        setTimeout(() => {

          window.location.href =
            link;

        }, 3500);

      }
    );

  });

}

/* ======================
   SEARCH SYSTEM
====================== */

const searchInput =
  document.querySelector(
    ".search-box input"
  );

const searchData = {

  "同意書": [
    {
      title: "新人役者募集項目",
      link:
        pathPrefix +
        "audition-guide.html"
    }
  ],

  "ライフスタイル": [
    {
      title: "公演について",
      link:
        pathPrefix +
        "performance.html"
    }
  ],

  "出荷": [
    {
      title: "出荷記録一覧",
      link:
        pathPrefix +
        "shipment-log.html"
    }
  ],

  "劇団員手引き": [
    {
      title: "劇団員手引き",
      link:
        pathPrefix +
        "member-guide.html"
    }
  ],

  "SNSアカウント": [
    {
      title: "卒業後対応マニュアル",
      link:
        pathPrefix +
        "graduate-manual.html"
    }
  ],

  "劇団員ページ": [

    {
      title: "劇団員ページ006",
      link:
        pathPrefix +
        "member-006.html"
    },

    {
      title: "劇団員ページ009",
      link:
        pathPrefix +
        "member-009.html"
    },

    {
      title: "劇団員ページ014",
      link:
        pathPrefix +
        "member-014.html"
    },

    {
      title: "劇団員ページ022",
      link:
        pathPrefix +
        "member-022.html"
    },

    {
      title: "劇団員ページ023",
      link:
        pathPrefix +
        "member-023.html"
    }

  ],

  "再演サービス": [
    {
      title: "再演依頼書",
      link:
        pathPrefix +
        "replay-request.html"
    }
  ],

  "アウトドア": [
    {
      title: "劇団員ページ026",
      link:
        pathPrefix +
        "member-026.html"
    }
  ],

  "家族": [
    {
      title: "記録_1",
      link:
        pathPrefix +
        "diary-001.html"
    }
  ],

  "信奉者": [
    {
      title: "劇団員ページ002",
      link:
        pathPrefix +
        "member-002.html"
    }
  ],

  "半生": [
    {
      title: "記録_2",
      link:
        pathPrefix +
        "diary-002.html"
    }
  ],

  "親友": [
    {
      title: "劇団員ページ003",
      link:
        pathPrefix +
        "member-003.html"
    }
  ],

  "蘇った": [
    {
      title: "記録_3",
      link:
        pathPrefix +
        "diary-003.html"
    }
  ],

  "美奈": [
    {
      title: "劇団員ページ001",
      link:
        pathPrefix +
        "member-001.html"
    }
  ],

  "次期公演": [
    {
      title: "次回再演依頼書",
      link:
        pathPrefix +
        "next-request.html"
    }
  ]

};

if (searchInput) {

  searchInput.addEventListener(
    "keydown",
    (event) => {

      if (event.key !== "Enter")
        return;

      event.preventDefault();

      const keyword =
        searchInput.value.trim();

      const result =
        searchData[keyword];

      let oldResults =
        document.querySelector(
          ".search-results"
        );

      if (oldResults) {

        oldResults.remove();

      }

      const resultBox =
        document.createElement(
          "div"
        );

      resultBox.className =
        "search-results info-box";

      if (result) {

        let html = `

          <h2>
            検索結果
          </h2>

          <p>
            ${result.length}件ヒットしました
          </p>

        `;

        result.forEach(item => {

          html += `

            <div class="search-result-item">

              <a href="${item.link}">
                ${item.title}
              </a>

            </div>

          `;

        });

        resultBox.innerHTML =
          html;

      }

      else {

        resultBox.innerHTML = `

          <h2>
            検索結果
          </h2>

          <p>
            検索結果がありません
          </p>

        `;

      }

      const main =
        document.querySelector(
          "main"
        );

      if (main) {

        main.prepend(
          resultBox
        );

        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });

      }

    }
  );

}