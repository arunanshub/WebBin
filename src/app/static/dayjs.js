dayjs.extend(window.dayjs_plugin_relativeTime);
dayjs.extend(window.dayjs_plugin_utc);

const elem = document.getElementById("relative_time");
const localTime = dayjs().to(
  dayjs(elem.getAttribute("data-relative-time")).utc(true).local()
);
document.getElementById("relative_time").textContent = localTime;
