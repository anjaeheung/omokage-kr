const accordions =
  document.querySelectorAll(
    ".accordion"
  );

accordions.forEach(
  (accordion) => {

    accordion.addEventListener(
      "click",
      () => {

        const panel =
          accordion.nextElementSibling;

        const isOpen =
          panel.style.display === "block";

        panel.style.display =
          isOpen
            ? "none"
            : "block";

      }
    );

  }
);

const subAccordions =
  document.querySelectorAll(
    ".sub-accordion"
  );

subAccordions.forEach(
  (accordion) => {

    accordion.addEventListener(
      "click",
      () => {

        const panel =
          accordion.nextElementSibling;

        const isOpen =
          panel.style.display === "block";

        panel.style.display =
          isOpen
            ? "none"
            : "block";

      }
    );

  }
);