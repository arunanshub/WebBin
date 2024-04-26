// disable submit button after the form has been submitted
window.addEventListener("DOMContentLoaded", (_) => {
    document.getElementById("form").onsubmit = () => {
      document.getElementById("submit").disabled = true;
      return true;
    };
  }, false);
