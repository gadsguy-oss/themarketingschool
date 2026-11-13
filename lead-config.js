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

/* ============ Conversion tracking ============
   Paste IDs to switch each one on. Blank = off. Main goal = quiz sign-up (the score gate). */
window.TMS_TRACKING = {
  GA4_ID: "",            // e.g. "G-XXXXXXXXXX"
  GOOGLE_ADS_ID: "",     // e.g. "AW-123456789"
  ADS_QUIZ_LABEL: "",    // conversion label for "Quiz sign-up" (primary)
  ADS_CONTACT_LABEL: "", // conversion label for "Package contact form" (secondary, optional)
  META_PIXEL_ID: ""      // e.g. "1234567890"
};
(function () {
  var t = window.TMS_TRACKING;
  if (t.GA4_ID || t.GOOGLE_ADS_ID) {
    var s = document.createElement("script"); s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + (t.GA4_ID || t.GOOGLE_ADS_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    if (t.GA4_ID) gtag("config", t.GA4_ID);
    if (t.GOOGLE_ADS_ID) gtag("config", t.GOOGLE_ADS_ID);
  }
  if (t.META_PIXEL_ID) {
    !function(f,b,e,v,n,t2,s2){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t2=b.createElement(e);t2.async=!0;t2.src=v;s2=b.getElementsByTagName(e)[0];s2.parentNode.insertBefore(t2,s2)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq("init", t.META_PIXEL_ID); fbq("track", "PageView");
  }
})();
/* kind: "quiz" (primary goal) or "contact" */
window.tmsConversion = function (kind, data) {
  var t = window.TMS_TRACKING || {}, d = data || {};
  try {
    if (typeof gtag === "function") {
      gtag("event", kind === "quiz" ? "quiz_signup" : "contact_form_submit", d);
      if (kind === "quiz") gtag("event", "generate_lead", { method: "quiz", value: d.score });
      var label = kind === "quiz" ? t.ADS_QUIZ_LABEL : t.ADS_CONTACT_LABEL;
      if (t.GOOGLE_ADS_ID && label) gtag("event", "conversion", { send_to: t.GOOGLE_ADS_ID + "/" + label });
    }
  } catch (e) {}
  try {
    if (typeof fbq === "function") {
      if (kind === "quiz") fbq("track", "Lead", { content_name: "Ad Account Score quiz" });
      else fbq("track", "Contact");
    }
  } catch (e) {}
};
