const bibSourceUrl = "assets/data/publications.bib";
const publicationGroups = [
  {
    id: "articles",
    title: "Peer-reviewed journal articles",
    matches: (entry) => entry.type === "article",
  },
  {
    id: "reports",
    title: "Non-peer-reviewed articles and reports",
    matches: (entry) => entry.type === "techreport",
  },
  {
    id: "presentations",
    title: "Presentations, lectures, and workshops",
    matches: (entry) => entry.type === "inproceedings",
  },
];

const escapeHtml = (value = "") =>
  value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const stripOuterBraces = (value) => {
  let output = value.trim();
  while (output.startsWith("{") && output.endsWith("}")) {
    output = output.slice(1, -1).trim();
  }
  return output;
};

const cleanValue = (value = "") =>
  stripOuterBraces(value)
    .replace(/\\&/g, "&")
    .replace(/[{}]/g, "")
    .replace(/\s+/g, " ")
    .trim();

const readBalanced = (text, start, openChar, closeChar) => {
  let depth = 0;
  let cursor = start;
  let output = "";

  for (; cursor < text.length; cursor += 1) {
    const char = text[cursor];
    if (char === openChar) {
      depth += 1;
      if (depth > 1) output += char;
      continue;
    }
    if (char === closeChar) {
      depth -= 1;
      if (depth === 0) break;
      output += char;
      continue;
    }
    output += char;
  }

  return { value: output, end: cursor + 1 };
};

const parseFields = (body) => {
  const fields = {};
  let cursor = 0;

  while (cursor < body.length) {
    while (cursor < body.length && /[\s,]/.test(body[cursor])) cursor += 1;
    const nameStart = cursor;
    while (cursor < body.length && /[A-Za-z0-9_-]/.test(body[cursor])) cursor += 1;
    const name = body.slice(nameStart, cursor).toLowerCase();
    if (!name) break;

    while (cursor < body.length && /\s/.test(body[cursor])) cursor += 1;
    if (body[cursor] !== "=") break;
    cursor += 1;
    while (cursor < body.length && /\s/.test(body[cursor])) cursor += 1;

    let value = "";
    if (body[cursor] === "{") {
      const result = readBalanced(body, cursor, "{", "}");
      value = result.value;
      cursor = result.end;
    } else if (body[cursor] === "\"") {
      const result = readBalanced(body, cursor, "\"", "\"");
      value = result.value;
      cursor = result.end;
    } else {
      const valueStart = cursor;
      while (cursor < body.length && body[cursor] !== ",") cursor += 1;
      value = body.slice(valueStart, cursor);
    }

    fields[name] = cleanValue(value);
  }

  return fields;
};

const parseBibtex = (source) => {
  const entries = [];
  let cursor = 0;

  while (cursor < source.length) {
    const at = source.indexOf("@", cursor);
    if (at === -1) break;
    const typeStart = at + 1;
    const braceStart = source.indexOf("{", typeStart);
    if (braceStart === -1) break;

    const type = source.slice(typeStart, braceStart).trim().toLowerCase();
    const result = readBalanced(source, braceStart, "{", "}");
    const body = result.value;
    const comma = body.indexOf(",");
    if (comma !== -1) {
      entries.push({
        type,
        key: body.slice(0, comma).trim(),
        fields: parseFields(body.slice(comma + 1)),
      });
    }
    cursor = result.end;
  }

  return entries;
};

const formatAuthor = (name) => {
  const trimmed = name.trim();
  if (!trimmed.includes(",")) return trimmed;
  const [last, ...rest] = trimmed.split(",");
  return `${rest.join(" ").trim()} ${last.trim()}`.replace(/\s+/g, " ").trim();
};

const formatAuthors = (authorField = "") =>
  authorField
    .split(/\s+and\s+/i)
    .map(formatAuthor)
    .filter(Boolean)
    .join(", ");

const formatVenue = ({ type, fields }) => {
  const parts = [];
  if (fields.journal) parts.push(`<em>${escapeHtml(fields.journal)}</em>`);
  if (fields.booktitle) parts.push(escapeHtml(fields.booktitle));
  if (fields.institution) parts.push(escapeHtml(fields.institution));

  const volumeNumber = [fields.volume, fields.number ? `(${fields.number})` : ""].filter(Boolean).join("");
  if (volumeNumber) parts.push(escapeHtml(volumeNumber));
  if (fields.pages) parts.push(`pp. ${escapeHtml(fields.pages)}`);
  if (fields.year) parts.push(escapeHtml(fields.year));

  if (type === "techreport" && !fields.institution) parts.unshift("Technical report");
  return parts.join(", ");
};

const renderEntry = (entry) => {
  const title = escapeHtml(entry.fields.title || "Untitled publication");
  const authors = escapeHtml(formatAuthors(entry.fields.author));
  const venue = formatVenue(entry);

  return `
    <li class="publication-entry">
      <h3>${title}</h3>
      ${authors ? `<p class="publication-authors">${authors}</p>` : ""}
      ${venue ? `<p class="publication-meta">${venue}</p>` : ""}
    </li>
  `;
};

const renderPublications = (entries) => {
  const root = document.querySelector("[data-publications-root]");
  const count = document.querySelector("[data-publication-count]");
  if (!root) return;

  const sorted = entries.slice().sort((a, b) => Number(b.fields.year || 0) - Number(a.fields.year || 0));
  if (count) count.textContent = `${entries.length} publications and presentations`;

  root.innerHTML = publicationGroups
    .map((group) => {
      const groupEntries = sorted.filter(group.matches);
      if (groupEntries.length === 0) return "";

      return `
        <section class="publication-group" id="${group.id}" aria-labelledby="${group.id}-heading">
          <div class="publication-group-heading">
            <h2 id="${group.id}-heading">${group.title}</h2>
            <span>${groupEntries.length}</span>
          </div>
          <ol class="publication-page-list">
            ${groupEntries.map(renderEntry).join("")}
          </ol>
        </section>
      `;
    })
    .join("");
};

const loadPublications = async () => {
  const root = document.querySelector("[data-publications-root]");
  if (!root) return;

  try {
    const response = await fetch(bibSourceUrl);
    if (!response.ok) throw new Error(`Unable to load ${bibSourceUrl}`);
    const entries = parseBibtex(await response.text());
    renderPublications(entries);
  } catch (error) {
    root.innerHTML = `
      <div class="publication-error">
        <h2>Publication list unavailable</h2>
        <p>The BibTeX source could not be loaded. You can still open the source file directly.</p>
        <a class="button button-outline" href="${bibSourceUrl}" download>Download BibTeX</a>
      </div>
    `;
  }
};

loadPublications();
