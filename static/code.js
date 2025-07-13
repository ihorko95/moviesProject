(function () {
  let ascending = true;

  function parseDate(dateStr) {

    if (typeof dateStr !== 'string') return new Date(2100, 0, 1);
    const parts = dateStr.trim().split(".");
    if (parts.length !== 2) return new Date(2100, 0, 1);
    const [day, month] = parts.map(Number);
    if (isNaN(day) || isNaN(month)) return new Date(2100, 0, 1);
    const now = new Date();
    const year =
      now.getMonth() + 1 > month ||
      (now.getMonth() + 1 === month && now.getDate() > day)
        ? now.getFullYear() + 1
        : now.getFullYear();
    return new Date(year, month - 1, day);
  }

  function sortRowsByDate() {
    const table = document.querySelector("table#pastable");
    if (!table) return;
    const tbody = table.querySelector("tbody");
    if (!tbody) return;

    const rows = Array.from(tbody.querySelectorAll("tr.acc-item.ng-scope"))
      .filter(row => !row.querySelector("td[style*='font-weight:bold']"));

    const rowMap = rows.map(row => {
      const dateSpan = row.querySelector("td:nth-child(2) span");
      const text = dateSpan ? dateSpan.textContent.trim() : "";
      const date = parseDate(text);
      return { row, date };
    });

    rowMap.sort((a, b) => ascending ? a.date - b.date : b.date - a.date);
    rowMap.forEach(({ row }) => tbody.appendChild(row));
    ascending = !ascending;
  }

  function addSortButton() {
    if (document.querySelector("#sortByDateBtn")) return;
    const table = document.querySelector("table#pastable");
    if (!table) return;

    const sortBtn = document.createElement("button");
    sortBtn.id = "sortByDateBtn";
    sortBtn.textContent = "Сортувати за датою ⬍";
    sortBtn.style = `
      margin: 10px;
      padding: 6px 12px;
      font-size: 14px;
      cursor: pointer;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
    `;
    sortBtn.onclick = sortRowsByDate;

    table.parentNode.insertBefore(sortBtn, table);

  }

  function addCopyButtons() {
    const table = document.querySelector("table#pastable");
    if (!table) return;
    const tbody = table.querySelector("tbody");
    if (!tbody) return;

    const rows = Array.from(tbody.querySelectorAll("tr.acc-item.ng-scope")).filter(row => !row.querySelector("td[style*='font-weight:bold']"));

    rows.forEach(row => {
      const routeCell = row.querySelector("td:nth-child(1)");
      const dateCell = row.querySelector("td:nth-child(2)");
      const nameCell = row.querySelector("td:nth-child(3)");
      const phoneCell = row.querySelector("td:nth-child(4)");

      if (!routeCell || !dateCell || !nameCell || !phoneCell) return;
      if (nameCell.querySelector(".copy-passenger-btn")) return;

      const routeText = routeCell.innerHTML
        .replace(/<br\s*\/?>/gi, "\n")
        .replace(/<\/?[^>]+(>|$)/g, "").trim();

      const date = dateCell.textContent.trim();
      const name = nameCell.querySelector("a")?.textContent.trim() || "";
      const phone = phoneCell.querySelector("span")?.textContent.trim() || "";

      const textToCopy = `${routeText}\n${date}\n${name}\n\`${phone}\``;


      const button = document.createElement("button");
      button.textContent = "📋 Копіювати";
      button.className = "copy-passenger-btn";
      button.style.cssText = `
        display: block;
        margin-top: 4px;
        font-size: 13px;
        background: #029EE4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 4px 6px;
        cursor: pointer;
      `;

      button.addEventListener("click", () => {
        navigator.clipboard.writeText(textToCopy).then(() => {
          button.textContent = "✅ Скопійовано!";
          setTimeout(() => {
            button.textContent = "📋 Копіювати";
          }, 1500);
        }).catch(err => {
          console.error("Помилка копіювання:", err);
          button.textContent = "❌ Помилка";
        });
      });

      nameCell.appendChild(button);
    });
  }

  function tryInit() {
    const table = document.querySelector("table#pastable");
    if (!table) return;

    addSortButton();
    addCopyButtons();
  }

  const observer = new MutationObserver(() => {
    tryInit();
  });

  observer.observe(document.body, { childList: true, subtree: true });

  // Спробувати відразу після завантаження
  setTimeout(tryInit, 2000);
})();

