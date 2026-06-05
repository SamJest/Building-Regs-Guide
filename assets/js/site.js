const routeAdvice = {
  full_plans: {
    title: "Likely route: full plans or early building-control discussion",
    confidence: "Medium",
    points: ["Best where structure, fire safety, drainage, ventilation or energy details need checking before work starts.", "Ask what drawings, calculations and specifications the building control body expects."],
    downloads: ["/downloads/building-notice-vs-full-plans-worksheet/", "/downloads/structural-calculations-briefing-sheet/"]
  },
  building_notice: {
    title: "Possible route: building notice",
    confidence: "Medium",
    points: ["Usually only worth considering for straightforward domestic work where the specification is already clear.", "You still need inspections and may carry more risk if details are found unsuitable during the build."],
    downloads: ["/downloads/building-notice-vs-full-plans-worksheet/", "/downloads/inspection-stage-record-sheet/"]
  },
  competent_person: {
    title: "Possible route: registered competent person",
    confidence: "Medium",
    points: ["Some electrical, heating, window and door work can be self-certified by a registered installer.", "Check registration before work starts and keep the certificate because it may matter on sale or remortgage."],
    downloads: ["/downloads/competent-person-certificate-checklist/", "/downloads/sale-remortgage-proof-folder/"]
  },
  regularisation: {
    title: "Likely route: regularisation or missing-evidence discussion",
    confidence: "Medium",
    points: ["For completed work with missing approval records, gather photos, invoices, drawings and certificates before contacting building control.", "Regularisation is not automatic and may require opening up work."],
    downloads: ["/downloads/regularisation-evidence-pack/", "/downloads/completion-certificate-record-sheet/"]
  },
  specialist: {
    title: "Stop route: specialist or BSR guidance first",
    confidence: "High",
    points: ["Do not use a homeowner shortcut for higher-risk buildings, flats, major fire-safety work or unclear structural risk.", "Speak to building control, a competent professional or the relevant regulator before relying on general guidance."],
    downloads: ["/downloads/building-control-phone-call-script/", "/downloads/sale-remortgage-proof-folder/"]
  }
};

const toolTweaks = {
  "full-plans-vs-building-notice-checker": values => values.structuralChange === "yes" || ["extension", "loft", "structural", "drainage"].includes(values.projectType) ? "full_plans" : "building_notice",
  "competent-person-scheme-checker": values => ["electrical", "heating", "windows"].includes(values.projectType) && values.workStatus !== "finished" ? "competent_person" : "full_plans",
  "completion-certificate-readiness-checker": values => values.certificateMissing === "yes" || values.workStatus === "finished" ? "regularisation" : "full_plans",
  "approved-document-router": values => values.higherRisk === "yes" ? "specialist" : "full_plans",
  "inspection-stage-checklist-generator": values => values.structuralChange === "yes" || ["extension", "loft", "garage", "drainage"].includes(values.projectType) ? "full_plans" : "building_notice",
  "jurisdiction-route-selector": values => values.jurisdiction !== "england" ? "specialist" : "full_plans"
};

const projectDocuments = {
  extension: ["Approved Document A", "Approved Document L", "Approved Document F", "Approved Document H"],
  loft: ["Approved Document A", "Approved Document B", "Approved Document K", "Approved Document L", "Approved Document F"],
  garage: ["Approved Document C", "Approved Document L", "Approved Document F", "Approved Document B"],
  structural: ["Approved Document A", "Approved Document B"],
  windows: ["Approved Document L", "Approved Document K", "Approved Document B"],
  electrical: ["Approved Document P"],
  heating: ["Approved Document L", "Approved Document F"],
  drainage: ["Approved Document H"]
};

const officialSources = [
  ["GOV.UK building regulations approval", "https://www.gov.uk/building-regulations-approval"],
  ["GOV.UK how to apply", "https://www.gov.uk/building-regulations-approval/how-to-apply"],
  ["GOV.UK competent person scheme", "https://www.gov.uk/building-regulations-approval/use-a-competent-person-scheme"],
  ["GOV.UK Approved Documents", "https://www.gov.uk/government/collections/approved-documents"]
];

function chooseRoute(values, toolSlug) {
  if (values.jurisdiction !== "england" || values.higherRisk === "yes") return "specialist";
  if (toolTweaks[toolSlug]) return toolTweaks[toolSlug](values);
  if (values.workStatus === "finished" || values.certificateMissing === "yes") return "regularisation";
  if (["electrical", "heating", "windows"].includes(values.projectType)) return "competent_person";
  if (values.structuralChange === "yes" || ["loft", "extension", "garage", "structural", "drainage"].includes(values.projectType)) return "full_plans";
  return "building_notice";
}

function renderResult(form) {
  const values = Object.fromEntries(new FormData(form).entries());
  const toolSlug = form.closest("[data-tool]")?.dataset.tool || "building-control-route-checker";
  const key = chooseRoute(values, toolSlug);
  const advice = routeAdvice[key];
  const docs = projectDocuments[values.projectType] || ["Approved Documents collection"];
  const target = form.parentElement.querySelector(".result");
  const date = new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
  target.innerHTML = `
    <h3>${advice.title}</h3>
    <p><strong>Confidence:</strong> ${advice.confidence}. This tool does not grant approval or replace building control, a designer, installer, engineer or registered approver.</p>
    <ul>${advice.points.map(point => `<li>${point}</li>`).join("")}</ul>
    <p><strong>Likely documents to check:</strong> ${docs.join(", ")}.</p>
    <p><strong>Red flags:</strong> higher-risk building, flat conversion, load-bearing changes, fire escape uncertainty, missing certificates, drainage changes, public sewer issues or work outside England.</p>
    <p><strong>Next actions:</strong> ask building control what they need before work starts, record who issues each certificate, and save evidence before work is covered up.</p>
    <p><strong>Official sources:</strong> ${officialSources.map(([label, url]) => `<a href="${url}">${label}</a>`).join(" / ")}</p>
    <p><strong>Recommended downloads:</strong> ${advice.downloads.map(path => `<a href="${path}">${path.split("/").filter(Boolean).pop().replaceAll("-", " ")}</a>`).join(" / ")}</p>
    <p class="local-note">Generated ${date}. Re-check official guidance before relying on this result.</p>
    <button class="button ghost" type="button" onclick="window.print()">Print</button>
    <button class="button ghost" type="button" data-save-result>Save locally</button>
  `;
  target.classList.add("show");
}

document.addEventListener("submit", event => {
  const form = event.target.closest("[data-tool-form]");
  if (!form) return;
  event.preventDefault();
  renderResult(form);
});

document.addEventListener("click", event => {
  if (!event.target.matches("[data-save-result]")) return;
  const result = event.target.closest(".result");
  const saved = JSON.parse(localStorage.getItem("brg_saved_results") || "[]");
  saved.push({ savedAt: new Date().toISOString(), text: result.innerText.slice(0, 1600) });
  localStorage.setItem("brg_saved_results", JSON.stringify(saved));
  event.target.textContent = "Saved locally";
});

document.addEventListener("DOMContentLoaded", () => {
  const mount = document.querySelector("[data-dashboard]");
  if (mount) {
    const saved = JSON.parse(localStorage.getItem("brg_saved_results") || "[]");
    const checklist = ["Route chosen", "Building control contacted", "Drawings/spec ready", "Inspection points recorded", "Certificates chased"];
    mount.innerHTML = `
      <article class="card"><h3>Project evidence tracker</h3><ul>${checklist.map((item, index) => `<li><label><input type="checkbox" data-dashboard-check="${index}"> ${item}</label></li>`).join("")}</ul><button class="button ghost" type="button" onclick="window.print()">Print dashboard</button></article>
      ${saved.length ? saved.map((item, index) => `<article class="card"><h3>Saved result ${index + 1}</h3><p class="local-note">${new Date(item.savedAt).toLocaleString("en-GB")}</p><p>${item.text.replace(/[<>&]/g, "")}</p></article>`).join("") : `<article class="card"><h3>No saved results yet</h3><p>Run a checker, save the result locally, then use this dashboard as your device-only evidence prompt.</p></article>`}
    `;
    document.querySelectorAll("[data-dashboard-check]").forEach(input => {
      input.checked = localStorage.getItem(`brg_check_${input.dataset.dashboardCheck}`) === "true";
      input.addEventListener("change", () => localStorage.setItem(`brg_check_${input.dataset.dashboardCheck}`, input.checked));
    });
  }
});