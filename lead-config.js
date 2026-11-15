/* The Marketing School — lead capture.
   Leads go to the "TMS Leads" Google Form, which feeds the "TMS Leads (Responses)" Google Sheet.
   The homepage package form, the quiz, and the contact page all use window.tmsSubmitLead(). */
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
   Vercel Web Analytics is the main analytics (custom events need a Vercel Pro plan).
   Ad platform slots stay blank until ads launch. Blank = nothing loads or fires.
   Main goal = quiz sign-up (the score gate). */
window.TMS_TRACKING = {
  GOOGLE_ADS_ID: "",     // e.g. "AW-123456789"  (fill in on ad launch day)
  ADS_QUIZ_LABEL: "",    // conversion label for "Quiz sign-up" (primary)
  ADS_CONTACT_LABEL: "", // conversion label for package form / contact form (secondary)
  META_PIXEL_ID: ""      // e.g. "1234567890"
};
(function () {
  var t = window.TMS_TRACKING;
  if (t.GOOGLE_ADS_ID) {
    var s = document.createElement("script"); s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + t.GOOGLE_ADS_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", t.GOOGLE_ADS_ID);
  }
  if (t.META_PIXEL_ID) {
    !function(f,b,e,v,n,t2,s2){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t2=b.createElement(e);t2.async=!0;t2.src=v;s2=b.getElementsByTagName(e)[0];s2.parentNode.insertBefore(t2,s2)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq("init", t.META_PIXEL_ID); fbq("track", "PageView");
  }
})();

/* One place every conversion fires from.
   kind: "quiz" (primary goal), "lead" (homepage package form), or "contact" (contact page). */
window.tmsConversion = function (kind, data) {
  var t = window.TMS_TRACKING || {}, d = data || {};
  var NAMES = { quiz: "quiz_signup", lead: "lead_form_submit", contact: "contact_form_submit" };
  var name = NAMES[kind] || kind;
  /* Vercel custom event: flat strings/numbers/booleans only */
  try {
    var flat = {};
    Object.keys(d).forEach(function (k) { var v = d[k]; if (v !== null && v !== undefined && typeof v !== "object") flat[k] = v; });
    if (typeof window.va === "function") window.va("event", { name: name, data: flat });
  } catch (e) {}
  /* Google Ads (only when the ID + label are filled in) */
  try {
    if (typeof gtag === "function" && t.GOOGLE_ADS_ID) {
      var label = kind === "quiz" ? t.ADS_QUIZ_LABEL : t.ADS_CONTACT_LABEL;
      if (label) gtag("event", "conversion", { send_to: t.GOOGLE_ADS_ID + "/" + label });
    }
  } catch (e) {}
  /* Meta (only when the pixel ID is filled in) */
  try {
    if (typeof fbq === "function") {
      if (kind === "quiz") fbq("track", "Lead", { content_name: "Ad Account Score quiz" });
      else if (kind === "lead") fbq("track", "Lead", { content_name: "Package form" });
      else fbq("track", "Contact");
    }
  } catch (e) {}
};
