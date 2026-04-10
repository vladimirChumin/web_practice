(() => {
  const form = document.getElementById("registerForm");
  if (!form) return;

  const checkUrl = form.dataset.checkUniqueUrl;
  if (!checkUrl) {
    console.error("Missing data-check-unique-url on #registerForm");
    return;
  }

  const usernameEl = document.getElementById("id_username");
  const emailEl = document.getElementById("id_email");
  const pass1El = document.getElementById("id_password1");

  const ensureErr = (input) => {
    let el = input.parentElement?.querySelector(".field-error");
    if (!el) {
      el = document.createElement("div");
      el.className = "field-error";
      input.insertAdjacentElement("afterend", el);
    }
    return el;
  };

  const setError = (input, msg) => {
    const errEl = ensureErr(input);
    errEl.textContent = msg || "";
    input.setAttribute("aria-invalid", msg ? "true" : "false");
  };

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const validateEmail = () => {
    if (!emailEl) return true;
    const v = (emailEl.value || "").trim();
    if (!v) return (setError(emailEl, "Введите email"), false);
    if (!emailRegex.test(v)) return (setError(emailEl, "Неверный формат email"), false);
    setError(emailEl, "");
    return true;
  };

  const validatePassword = () => {
    if (!pass1El) return true;
    const v = pass1El.value || "";
    if (v.length < 6) return (setError(pass1El, "Пароль должен быть не меньше 6 символов"), false);
    setError(pass1El, "");
    return true;
  };

  const validateUsername = () => {
    if (!usernameEl) return true;
    const v = (usernameEl.value || "").trim();
    if (!v) return (setError(usernameEl, "Введите логин"), false);
    setError(usernameEl, "");
    return true;
  };

  const checkUnique = async (field, value) => {
    try {
      const url = new URL(checkUrl, window.location.origin);
      url.searchParams.set("field", field);
      url.searchParams.set("value", value);

      const res = await fetch(url.toString(), {
        method: "GET",
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });

      if (!res.ok) return { ok: false, error: `HTTP ${res.status}` };

      const data = await res.json();
      if (typeof data?.available !== "boolean") {
        return { ok: false, error: "Bad JSON shape" };
      }

      return { ok: true, available: data.available };
    } catch (err) {
      return { ok: false, error: String(err) };
    }
  };

  let uReq = 0;
  let eReq = 0;

  const checkUsernameUnique = async () => {
    if (!usernameEl) return true;
    if (!validateUsername()) return false;

    const val = usernameEl.value.trim();
    const reqId = ++uReq;

    const data = await checkUnique("username", val);
    if (reqId !== uReq) return false;

    if (!data.ok) return (setError(usernameEl, "Не удалось проверить логин"), false);
    if (data.available === false) return (setError(usernameEl, "Логин уже занят"), false);

    setError(usernameEl, "");
    return true;
  };

  const checkEmailUnique = async () => {
    if (!emailEl) return true;
    if (!validateEmail()) return false;

    const val = emailEl.value.trim();
    const reqId = ++eReq;

    const data = await checkUnique("email", val);
    if (reqId !== eReq) return false;

    if (!data.ok) return (setError(emailEl, "Не удалось проверить email"), false);
    if (data.available === false) return (setError(emailEl, "Email уже используется"), false);

    setError(emailEl, "");
    return true;
  };

  usernameEl?.addEventListener("blur", () => void checkUsernameUnique());
  emailEl?.addEventListener("blur", () => void checkEmailUnique());
  emailEl?.addEventListener("input", validateEmail);
  pass1El?.addEventListener("input", validatePassword);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const okLocal = validateUsername() && validateEmail() && validatePassword();
    if (!okLocal) return;

    const [okU, okE] = await Promise.all([checkUsernameUnique(), checkEmailUnique()]);
    if (okU && okE) form.submit();
  });
})();
