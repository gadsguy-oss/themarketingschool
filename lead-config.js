/* The Marketing School — lead capture.
   Leads go to the "TMS Leads" Google Form, which feeds the "TMS Leads (Responses)" Google Sheet.
   Both the homepage package form and the quiz use window.tmsSubmitLead(). */
window.TMS_LEAD_FORM = {
  action: "https://docs.google.com/forms/d/e/1FAIpQLSfPG5OeweXCB8mbxcgnWfqCv4C688Kq19rUXihiZaW5TPD1nA/formResponse",
  fields: {
    source: "entry.1186201269", name: "entry.331545548", email: "entry.1030511994", phone: "entry.1335740292",
    contact_pref: "entry.1547025455", ad_spend: "entry.1593650914", package: "entry.527298381",
    quiz_score: "entry.627352898", website: "entry.2048602674", details: "entry.1486540982", tracking: "entry.2024198283"
  }
};
window.tmsSubmitLead = function (lead) {
  var cfg = window.TMS_LEAD_FORM, body = new URLSearchParams();
  Object.keys(cfg.fields).forEach(function (k) {
    var v = lead[k];
    if (v !== undefined && v !== null && v !== "") body.append(cfg.fields[k], String(v));
  });
  return fetch(cfg.action, { method: "POST", mode: "no-cors", body: body, keepalive: true });
};
