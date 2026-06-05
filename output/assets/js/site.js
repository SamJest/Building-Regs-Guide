const routeAdvice = {
  full_plans: {
    title: "Likely route: full plans or early building control discussion",
    confidence: "Medium",
    points: ["Useful where structure, fire safety, drainage or energy details need checking before work starts.", "Ask what drawings, calculations and specifications the building control body expects."]
  },
  building_notice: {
    title: "Possible route: building notice",
    confidence: "Medium",
    points: ["Often used for smaller domestic work where the details are straightforward.", "You still need inspections and you carry more risk if details are found unsuitable during the build."]
  },
  competent_person: {
    title: "Possible route: registered competent person",
    confidence: "Medium",
    points: ["Some electrical, heating, window and door work can be self-certified by a registered installer.", "Check the installer registration before work starts and keep the certificate."]
  },
  regularisation: {
    title: "Likely route: regularisation or missing-evidence discussion",
    confidence: "Medium",
    points: ["For completed work with missing approval records, gather photos, invoices, drawings and certificates before contacting building control.", "Regularisation is not automatic and may require opening up work."]
  },
  specialist: {
    title: "Stop route: specialist or BSR guidance first",
    confidence: "High",
    points: ["Do not use a homeowner shortcut for higher-risk buildings, flats, major fire-safety work or unclear structural risk.", "Speak to building control, a competent professional or the relevant regulator before relying on general guidance."]
  }
};

function chooseRoute(values) {
  if (values.jurisdiction !== "england" || values.higherRisk === "yes") return "specialist";
  if (values.workStatus === "finished" || values.certificateMissing === "yes") return "regularisation";
  if (values.projectType === "electrical" || values.projectType === "heating" || values.projectType === "windows") return "competent_person";
  if (values.structuralChange === "yes" || values.projectType === "loft" || values.projectType === "extension") return "full_plans";
  return "building_notice";
}

function renderResult(form) {
  const values = Object.fromEntries(new FormData(form).entries());
  const key = chooseRoute(values);
  const advice = routeAdvice[key];
  const target = form.parentElement.querySelector(".result");
  const date = new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
  target.innerHTML = `
    <h3>${advice.title}</h3>
    <p><strong>Confidence:</strong> ${advice.confidence}. This tool gives a planning prompt for your next conversation; it does not grant approval or replace building control.</p>
    <ul>${advice.points.map(point => `<li>${point}</li>`).join("")}</ul>
    <p><strong>Red flags:</strong> higher-risk building, flat conversion, load-bearing changes, fire escape uncertainty, missing certificates, drainage changes or work outside England.</p>
    <p><strong>Next actions:</strong> save this result, check the official source links on this page, and ask your building control body what they need before work starts.</p>
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
    mount.innerHTML = saved.length ? saved.map((item, index) => `<article class="card"><h3>Saved result ${index + 1}</h3><p class="local-note">${new Date(item.savedAt).toLocaleString("en-GB")}</p><p>${item.text.replace(/[<>&]/g, "")}</p></article>`).join("") : `<p>No saved tool results on this device yet.</p>`;
  }
});