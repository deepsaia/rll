document$.subscribe(function () {
  const form = document.forms.feedback;
  if (!form) return;

  form.hidden = false;

  // Ensure buttons are type="button" (optional but safe)
  form.querySelectorAll(".md-feedback__icon").forEach(btn => {
    btn.setAttribute("type", "button");
  });

  form.addEventListener("submit", function (ev) {
    ev.preventDefault(); // Always prevent submission
  });

  form.addEventListener("click", function (ev) {
    if (ev.target.matches(".md-feedback__icon")) {
      const data = ev.target.getAttribute("data-md-value");
      const note = form.querySelector(`.md-feedback__note[data-md-value="${data}"]`);
      if (note) note.hidden = false;

      console.log("Feedback:", { page: location.pathname, rating: data });
    }
  });
});