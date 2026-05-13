const API_BASE = "http://127.0.0.1:5000";

const els = {
  serverStatus: document.getElementById("serverStatus"),
  statProducts: document.getElementById("statProducts"),
  statTriples: document.getElementById("statTriples"),
  statFilters: document.getElementById("statFilters"),

  keywordInput: document.getElementById("keywordInput"),
  skinTypeSelect: document.getElementById("skinTypeSelect"),
  concernSelect: document.getElementById("concernSelect"),
  ingredientSelect: document.getElementById("ingredientSelect"),
  brandSelect: document.getElementById("brandSelect"),
  categorySelect: document.getElementById("categorySelect"),
  benefitSelect: document.getElementById("benefitSelect"),
  priceRangeSelect: document.getElementById("priceRangeSelect"),
  searchBtn: document.getElementById("searchBtn"),
  resetBtn: document.getElementById("resetBtn"),

  resultTitle: document.getElementById("resultTitle"),
  resultCount: document.getElementById("resultCount"),
  activeFilters: document.getElementById("activeFilters"),
  loadingState: document.getElementById("loadingState"),
  errorState: document.getElementById("errorState"),
  productGrid: document.getElementById("productGrid"),

  sparqlInput: document.getElementById("sparqlInput"),
  runSparqlBtn: document.getElementById("runSparqlBtn"),
  clearSparqlBtn: document.getElementById("clearSparqlBtn"),
  sparqlCount: document.getElementById("sparqlCount"),
  sparqlError: document.getElementById("sparqlError"),
  sparqlTableWrap: document.getElementById("sparqlTableWrap"),

  detailModal: document.getElementById("detailModal"),
  modalCloseBtn: document.getElementById("modalCloseBtn"),
  modalContent: document.getElementById("modalContent"),
};

const filterMap = {
  skin_type: { select: els.skinTypeSelect, label: "Skin Type" },
  concern: { select: els.concernSelect, label: "Concern" },
  ingredient: { select: els.ingredientSelect, label: "Ingredient" },
  brand: { select: els.brandSelect, label: "Brand" },
  category: { select: els.categorySelect, label: "Category" },
  benefit: { select: els.benefitSelect, label: "Benefit" },
  price_range: { select: els.priceRangeSelect, label: "Price Range" },
};

const examples = {
  allProducts: `PREFIX beauty: <http://beautygraph.org/ontology#>

SELECT ?product ?name
WHERE {
  ?product a beauty:Product ;
           beauty:productName ?name .
}
ORDER BY ?product
LIMIT 10`,

  niacinamide: `PREFIX beauty: <http://beautygraph.org/ontology#>

SELECT ?product ?name ?brand
WHERE {
  ?product a beauty:Product ;
           beauty:productName ?name ;
           beauty:hasIngredient beauty:Niacinamide ;
           beauty:belongsToBrand ?brand .
}
ORDER BY ?brand ?name
LIMIT 15`,

  oilyAcne: `PREFIX beauty: <http://beautygraph.org/ontology#>

SELECT ?product ?name ?brand ?category
WHERE {
  ?product a beauty:Product ;
           beauty:productName ?name ;
           beauty:suitableFor beauty:OilySkin ;
           beauty:targetsConcern beauty:Acne ;
           beauty:belongsToBrand ?brand ;
           beauty:belongsToCategory ?category .
}
ORDER BY ?brand ?name
LIMIT 15`,

  similar: `PREFIX beauty: <http://beautygraph.org/ontology#>

SELECT ?candidate ?candidateName
       (COUNT(DISTINCT ?sharedIngredient) AS ?sharedIngredientCount)
       (GROUP_CONCAT(DISTINCT ?sharedIngredient; separator=", ") AS ?sharedIngredients)
WHERE {
  beauty:P001 beauty:hasIngredient ?sharedIngredient .

  ?candidate a beauty:Product ;
             beauty:productName ?candidateName ;
             beauty:hasIngredient ?sharedIngredient .

  FILTER(?candidate != beauty:P001)
}
GROUP BY ?candidate ?candidateName
HAVING (COUNT(DISTINCT ?sharedIngredient) >= 2)
ORDER BY DESC(?sharedIngredientCount)
LIMIT 10`,
};

function setStatus(type, text) {
  const dotClass =
    type === "ok" ? "status-ok" : type === "error" ? "status-error" : "status-pending";

  els.serverStatus.innerHTML = `
    <span class="status-dot ${dotClass}"></span>
    <span>${escapeHtml(text)}</span>
  `;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function getNodeValue(node) {
  if (!node) return "";
  if (typeof node === "string") return node;
  return node.value ?? node.label ?? node.localName ?? "";
}

function getNodeLabel(node) {
  if (!node) return "";
  if (typeof node === "string") return node;
  return node.label ?? node.value ?? node.localName ?? "";
}

function getLocalNameFromUri(uri) {
  const text = String(uri ?? "");
  if (text.includes("#")) return text.split("#").pop();
  return text.split("/").pop();
}

function humanizeIdentifier(value) {
  return String(value ?? "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/\s+/g, " ")
    .trim();
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => null);

  if (!response.ok || data?.success === false) {
    throw new Error(data?.error || `Request failed with status ${response.status}`);
  }

  return data;
}

async function init() {
  bindEvents();
  els.sparqlInput.value = examples.allProducts;

  try {
    await checkHealth();
    await loadFilters();
    await searchProducts();
  } catch (error) {
    setStatus("error", "Backend error");
    showError(error.message);
  }
}

function bindEvents() {
  document.querySelectorAll(".tab-btn").forEach((button) => {
    button.addEventListener("click", () => switchTab(button.dataset.tab));
  });

  els.searchBtn.addEventListener("click", searchProducts);
  els.resetBtn.addEventListener("click", resetFilters);
  els.keywordInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") searchProducts();
  });

  els.runSparqlBtn.addEventListener("click", runSparqlDemo);
  els.clearSparqlBtn.addEventListener("click", () => {
    els.sparqlTableWrap.innerHTML = "";
    els.sparqlCount.textContent = "0 rows";
    els.sparqlError.classList.add("hidden");
  });

  document.querySelectorAll("[data-example]").forEach((button) => {
    button.addEventListener("click", () => {
      els.sparqlInput.value = examples[button.dataset.example] || examples.allProducts;
    });
  });

  els.modalCloseBtn.addEventListener("click", closeModal);
  els.detailModal.addEventListener("click", (event) => {
    if (event.target === els.detailModal) closeModal();
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tabId);
  });

  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === tabId);
  });
}

async function checkHealth() {
  const health = await fetchJson(`${API_BASE}/health`);

  els.statProducts.textContent = health.totalProducts ?? "-";
  els.statTriples.textContent = health.totalTriples ?? "-";
  setStatus("ok", "Backend connected");
}

async function loadFilters() {
  const response = await fetchJson(`${API_BASE}/filters`);
  const data = response.data || {};

  fillSelect(els.skinTypeSelect, data.skinTypes || [], "Semua Skin Type");
  fillSelect(els.concernSelect, data.concerns || [], "Semua Concern");
  fillSelect(els.ingredientSelect, data.ingredients || [], "Semua Ingredient");
  fillSelect(els.brandSelect, data.brands || [], "Semua Brand");
  fillSelect(els.categorySelect, data.categories || [], "Semua Category");
  fillSelect(els.benefitSelect, data.benefits || [], "Semua Benefit");
  fillSelect(els.priceRangeSelect, data.priceRanges || [], "Semua Price Range");

  const totalOptions = Object.values(data).reduce((sum, items) => sum + (items?.length || 0), 0);
  els.statFilters.textContent = totalOptions;
}

function fillSelect(select, items, placeholder) {
  select.innerHTML = `<option value="">${escapeHtml(placeholder)}</option>`;

  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.label;
    select.appendChild(option);
  });
}

function getFilters() {
  const filters = {};

  Object.entries(filterMap).forEach(([key, config]) => {
    const value = config.select.value;
    if (value) filters[key] = value;
  });

  return filters;
}

function buildProductUrl(filters) {
  const params = new URLSearchParams();
  params.set("limit", "100");

  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });

  return `${API_BASE}/products?${params.toString()}`;
}

async function searchProducts() {
  const filters = getFilters();

  showLoading(true);
  hideError();
  els.productGrid.innerHTML = "";

  try {
    const response = await fetchJson(buildProductUrl(filters));
    let rows = response.data?.results || [];

    const keyword = els.keywordInput.value.trim().toLowerCase();
    if (keyword) {
      rows = rows.filter((row) =>
        getNodeValue(row.productName).toLowerCase().includes(keyword)
      );
    }

    renderActiveFilters(filters, keyword);
    renderProducts(rows);
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
}

function renderActiveFilters(filters, keyword) {
  const pills = [];

  if (keyword) {
    pills.push(`Keyword: ${keyword}`);
  }

  Object.entries(filters).forEach(([key, value]) => {
    const label = filterMap[key]?.label || key;
    pills.push(`${label}: ${humanizeIdentifier(value)}`);
  });

  els.activeFilters.innerHTML = pills
    .map((pill) => `<span class="filter-pill">${escapeHtml(pill)}</span>`)
    .join("");
}

function renderProducts(rows) {
  els.resultCount.textContent = `${rows.length} hasil`;
  els.resultTitle.textContent = rows.length ? "Produk ditemukan" : "Tidak ada produk";

  if (!rows.length) {
    els.productGrid.innerHTML = `
      <div class="state-card">
        <p>Tidak ada produk yang cocok dengan filter saat ini.</p>
      </div>
    `;
    return;
  }

  els.productGrid.innerHTML = rows.map(productCardHtml).join("");

  document.querySelectorAll("[data-detail-id]").forEach((button) => {
    button.addEventListener("click", () => openProductDetail(button.dataset.detailId));
  });
}

function productCardHtml(row) {
  const productName = getNodeValue(row.productName);
  const productId = getNodeLabel(row.product);
  const brand = getNodeValue(row.brandName);
  const category = getNodeValue(row.categoryName);
  const price = getNodeValue(row.priceRangeName);
  const source = getNodeValue(row.sourceURL);

  return `
    <article class="product-card">
      <div class="meta-row">
        <span class="meta">${escapeHtml(productId)}</span>
        <span class="meta">${escapeHtml(category)}</span>
        <span class="meta">${escapeHtml(price)}</span>
      </div>

      <h4>${escapeHtml(productName)}</h4>
      <p class="eyebrow">${escapeHtml(brand)}</p>

      <a class="source-link" href="${escapeHtml(source)}" target="_blank" rel="noopener noreferrer">
        Lihat sumber produk →
      </a>

      <button class="detail-btn" data-detail-id="${escapeHtml(productId)}">
        Lihat Detail Semantik
      </button>
    </article>
  `;
}

function resetFilters() {
  els.keywordInput.value = "";
  Object.values(filterMap).forEach((config) => {
    config.select.value = "";
  });
  searchProducts();
}

function showLoading(isLoading) {
  els.loadingState.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  els.errorState.textContent = message;
  els.errorState.classList.remove("hidden");
}

function hideError() {
  els.errorState.classList.add("hidden");
  els.errorState.textContent = "";
}

async function runSparqlDemo() {
  const query = els.sparqlInput.value.trim();
  els.sparqlError.classList.add("hidden");
  els.sparqlTableWrap.innerHTML = "";
  els.sparqlCount.textContent = "Running...";

  try {
    const response = await fetchJson(`${API_BASE}/sparql`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    renderSparqlResult(response.data);
  } catch (error) {
    els.sparqlCount.textContent = "0 rows";
    els.sparqlError.textContent = error.message;
    els.sparqlError.classList.remove("hidden");
  }
}

function renderSparqlResult(data) {
  if (!data) {
    els.sparqlCount.textContent = "0 rows";
    els.sparqlTableWrap.innerHTML = "";
    return;
  }

  if (data.type === "ASK") {
    els.sparqlCount.textContent = "ASK";
    els.sparqlTableWrap.innerHTML = `<div class="state-card">Result: ${data.boolean}</div>`;
    return;
  }

  if (data.type === "CONSTRUCT" || data.type === "DESCRIBE") {
    els.sparqlCount.textContent = `${data.tripleCount} triples`;
    els.sparqlTableWrap.innerHTML = `<pre class="ontology-diagram">${escapeHtml(data.turtle)}</pre>`;
    return;
  }

  const variables = data.variables || [];
  const rows = data.results || [];
  els.sparqlCount.textContent = `${rows.length} rows`;

  if (!rows.length) {
    els.sparqlTableWrap.innerHTML = `<div class="state-card">Query berhasil, tetapi tidak ada hasil.</div>`;
    return;
  }

  els.sparqlTableWrap.innerHTML = `
    <table>
      <thead>
        <tr>${variables.map((v) => `<th>${escapeHtml(v)}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows
          .map((row) => `
            <tr>
              ${variables
                .map((variable) => {
                  const node = row[variable];
                  const text = node?.type === "uri"
                    ? `${node.label || node.localName}`
                    : getNodeValue(node);

                  const fullValue = getNodeValue(node);
                  const className = String(fullValue).startsWith("http") ? "uri-cell" : "";

                  return `<td class="${className}" title="${escapeHtml(fullValue)}">${escapeHtml(text)}</td>`;
                })
                .join("")}
            </tr>
          `)
          .join("")}
      </tbody>
    </table>
  `;
}

async function openProductDetail(productId) {
  const query = buildProductDetailQuery(productId);

  els.modalContent.innerHTML = `
    <div class="detail-content">
      <div class="state-card">
        <div class="loader"></div>
        <p>Mengambil detail semantik produk...</p>
      </div>
    </div>
  `;
  els.detailModal.classList.remove("hidden");

  try {
    const response = await fetchJson(`${API_BASE}/sparql`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const row = response.data?.results?.[0];
    if (!row) {
      throw new Error("Detail produk tidak ditemukan.");
    }

    renderProductDetail(productId, row);
  } catch (error) {
    els.modalContent.innerHTML = `
      <div class="detail-content">
        <div class="state-card error">${escapeHtml(error.message)}</div>
      </div>
    `;
  }
}

function buildProductDetailQuery(productId) {
  const safeId = String(productId).replace(/[^A-Za-z0-9_]/g, "");

  return `PREFIX beauty: <http://beautygraph.org/ontology#>

SELECT ?productName ?brandName ?categoryName ?priceRangeName ?sourceURL
       (GROUP_CONCAT(DISTINCT ?ingredientName; separator=", ") AS ?ingredients)
       (GROUP_CONCAT(DISTINCT ?skinTypeName; separator=", ") AS ?skinTypes)
       (GROUP_CONCAT(DISTINCT ?concernName; separator=", ") AS ?concerns)
       (GROUP_CONCAT(DISTINCT ?benefitName; separator=", ") AS ?benefits)
WHERE {
  beauty:${safeId} a beauty:Product ;
                 beauty:productName ?productName ;
                 beauty:belongsToBrand ?brand ;
                 beauty:belongsToCategory ?category ;
                 beauty:hasPriceRange ?priceRange ;
                 beauty:sourceURL ?sourceURL ;
                 beauty:hasIngredient ?ingredient ;
                 beauty:suitableFor ?skinType ;
                 beauty:targetsConcern ?concern ;
                 beauty:hasBenefit ?benefit .

  BIND(REPLACE(STRAFTER(STR(?brand), "#"), "([a-z])([A-Z])", "$1 $2") AS ?brandName)
  BIND(STRAFTER(STR(?category), "#") AS ?categoryName)
  BIND(STRAFTER(STR(?priceRange), "#") AS ?priceRangeName)
  BIND(REPLACE(STRAFTER(STR(?ingredient), "#"), "([a-z])([A-Z])", "$1 $2") AS ?ingredientName)
  BIND(REPLACE(STRAFTER(STR(?skinType), "#"), "([a-z])([A-Z])", "$1 $2") AS ?skinTypeName)
  BIND(REPLACE(STRAFTER(STR(?concern), "#"), "([a-z])([A-Z])", "$1 $2") AS ?concernName)
  BIND(REPLACE(STRAFTER(STR(?benefit), "#"), "([a-z])([A-Z])", "$1 $2") AS ?benefitName)
}
GROUP BY ?productName ?brandName ?categoryName ?priceRangeName ?sourceURL`;
}

function renderProductDetail(productId, row) {
  const productName = getNodeValue(row.productName);
  const brand = getNodeValue(row.brandName);
  const category = getNodeValue(row.categoryName);
  const price = getNodeValue(row.priceRangeName);
  const source = getNodeValue(row.sourceURL);
  const ingredients = getNodeValue(row.ingredients);
  const skinTypes = getNodeValue(row.skinTypes);
  const concerns = getNodeValue(row.concerns);
  const benefits = getNodeValue(row.benefits);

  els.modalContent.innerHTML = `
    <div class="detail-content">
      <p class="eyebrow">${escapeHtml(productId)} • Semantic Product Detail</p>
      <h3>${escapeHtml(productName)}</h3>
      <p>
        Detail ini diambil dari RDF melalui endpoint <code>POST /sparql</code>.
      </p>

      <div class="detail-grid">
        ${detailBox("Brand", brand)}
        ${detailBox("Category", category)}
        ${detailBox("Price Range", price)}
        ${detailBox("Source URL", `<a href="${escapeHtml(source)}" target="_blank" rel="noopener noreferrer">Open source</a>`, true)}
        ${detailBox("Ingredients", ingredients)}
        ${detailBox("Suitable For", skinTypes)}
        ${detailBox("Targets Concern", concerns)}
        ${detailBox("Benefits", benefits)}
      </div>

      <div class="graph-box">
        <div class="graph-title">Knowledge Graph View</div>
        <div class="kg-graph">
          <span class="kg-node product-node">${escapeHtml(productName)}</span>
          ${kgNodes("Brand", brand)}
          ${kgNodes("Category", category)}
          ${kgNodes("Ingredient", ingredients)}
          ${kgNodes("SkinType", skinTypes)}
          ${kgNodes("Concern", concerns)}
          ${kgNodes("Benefit", benefits)}
          ${kgNodes("PriceRange", price)}
        </div>
      </div>
    </div>
  `;
}

function detailBox(label, value, raw = false) {
  return `
    <div class="detail-box">
      <span>${escapeHtml(label)}</span>
      ${raw ? value : escapeHtml(value || "-")}
    </div>
  `;
}

function kgNodes(prefix, csv) {
  return String(csv || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => `<span class="kg-node">${escapeHtml(prefix)}: ${escapeHtml(item)}</span>`)
    .join("");
}

function closeModal() {
  els.detailModal.classList.add("hidden");
}

init();
