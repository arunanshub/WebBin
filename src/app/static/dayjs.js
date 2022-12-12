dayjs.extend(window.dayjs_plugin_relativeTime);
dayjs.extend(window.dayjs_plugin_utc);
dayjs.extend(window.dayjs_plugin_localizedFormat);

window.addEventListener("DOMContentLoaded", (_) => {
  const elem = document.getElementById("created_at");
  const localTime = dayjs(elem.getAttribute("data-created-at")).utc(true).local();
  elem.textContent = localTime.format("ll");
}, false);
