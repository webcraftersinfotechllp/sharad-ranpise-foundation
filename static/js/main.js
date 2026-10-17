document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      const isOpen = navMenu.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  const faqButtons = document.querySelectorAll(".faq-question");
  faqButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const item = button.closest(".faq-item");
      if (!item) return;

      const isOpen = item.classList.contains("active");
      faqButtons.forEach((btn) => {
        const parent = btn.closest(".faq-item");
        if (parent) {
          parent.classList.remove("active");
          btn.setAttribute("aria-expanded", "false");
        }
      });

      if (!isOpen) {
        item.classList.add("active");
        button.setAttribute("aria-expanded", "true");
      }
    });
  });

  const galleryItems = document.querySelectorAll(".gallery-item");
  const lightbox = document.querySelector(".lightbox");

  if (lightbox) {
    const lightboxImage = lightbox.querySelector("img");
    const lightboxClose = lightbox.querySelector(".lightbox-close");

    galleryItems.forEach((item) => {
      item.addEventListener("click", function () {
        const image = item.querySelector("img");
        if (!image || !lightboxImage) return;
        lightboxImage.src = image.src;
        lightboxImage.alt = image.alt || "Selected gallery item";
        lightbox.classList.add("open");
      });
    });

    lightboxClose.addEventListener("click", function () {
      lightbox.classList.remove("open");
    });

    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox) {
        lightbox.classList.remove("open");
      }
    });
  }

  const amountButtons = document.querySelectorAll(".amount-button");
  const donationForm = document.querySelector("#donation-form");
  if (donationForm) {
    const formAmount = donationForm.querySelector("#amount");
    const customAmount = donationForm.querySelector("#custom-amount");
    const purposeInput = donationForm.querySelector("#purpose");
    const nameInput = donationForm.querySelector("#name");
    const summaryAmount = donationForm.querySelector("#summary-amount");
    const summaryTotal = donationForm.querySelector("#summary-total");
    const summaryPurpose = donationForm.querySelector("#summary-purpose");
    const summaryDonor = donationForm.querySelector("#summary-donor");
    const formatAmount = (value) =>
      value ? `₹${Number(value).toLocaleString("en-IN")}` : "₹0";

    const updateDonationSummary = () => {
      const value = formAmount?.value || "";
      if (summaryAmount) summaryAmount.textContent = formatAmount(value);
      if (summaryTotal) summaryTotal.textContent = formatAmount(value);
      if (summaryPurpose)
        summaryPurpose.textContent = purposeInput?.value || "Select a focus";
      if (summaryDonor)
        summaryDonor.textContent = nameInput?.value || "Your name";
    };

    amountButtons.forEach((button) =>
      button.addEventListener("click", () => {
        const value = button.dataset.amount || "";
        amountButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");
        if (formAmount) formAmount.value = value;
        if (customAmount) customAmount.value = "";
        updateDonationSummary();
      }),
    );

    customAmount?.addEventListener("input", () => {
      if (formAmount) formAmount.value = customAmount.value;
      amountButtons.forEach((button) =>
        button.classList.toggle(
          "active",
          button.dataset.amount === customAmount.value,
        ),
      );
      updateDonationSummary();
    });
    nameInput?.addEventListener("input", updateDonationSummary);
    donationForm.querySelectorAll(".purpose-option").forEach((option) =>
      option.addEventListener("click", () => {
        donationForm.querySelectorAll(".purpose-option").forEach((item) => {
          item.classList.remove("active");
          item.setAttribute("aria-pressed", "false");
        });
        option.classList.add("active");
        option.setAttribute("aria-pressed", "true");
        if (purposeInput) purposeInput.value = option.dataset.purpose || "";
        updateDonationSummary();
      }),
    );
    updateDonationSummary();
  }

  const counters = document.querySelectorAll(".counter");
  const animateCounter = (element) => {
    const target = Number(element.dataset.target || 0);
    const suffix = element.dataset.suffix || "";
    let current = 0;
    const increment = Math.max(1, Math.ceil(target / 80));

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      element.textContent = `${current}${suffix}`;
    }, 20);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const element = entry.target;
          if (!element.dataset.animated) {
            element.dataset.animated = "true";
            animateCounter(element);
          }
        }
      });
    },
    { threshold: 0.4 },
  );

  counters.forEach((counter) => observer.observe(counter));

  const onlyLettersAndSpaces = /^[A-Za-z\s]+$/;
  const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const validMobile = /^[6-9]\d{9}$/;
  const positiveInteger = /^[1-9]\d*$/;

  function setFieldError(input, message, errorElement) {
    if (!input) return false;
    const error =
      errorElement || input.parentElement.querySelector(".error-msg");
    const invalid = Boolean(message);
    input.setAttribute("aria-invalid", String(invalid));
    input.classList.toggle("input-invalid", invalid);
    if (error) {
      error.textContent = message || "";
      error.hidden = !invalid;
    }
    return !invalid;
  }

  function validateContactForm(form) {
    if (!form) return true;
    const fields = {
      name: form.querySelector("#name"),
      email: form.querySelector("#email"),
      mobile: form.querySelector("#mobile"),
      subject: form.querySelector("#subject"),
      message: form.querySelector("#message"),
    };
    const errors = {
      name: "Enter a name using letters and spaces only.",
      email: "Enter a valid email address.",
      mobile: "Enter exactly 10 digits starting with 6, 7, 8, or 9.",
      subject: "Enter a subject using letters and spaces only.",
      message: "Message must be at least 10 characters long.",
    };
    let valid = true;
    const checks = {
      name:
        fields.name &&
        fields.name.value.trim().length >= 3 &&
        onlyLettersAndSpaces.test(fields.name.value.trim()),
      email: fields.email && validEmail.test(fields.email.value.trim()),
      mobile: fields.mobile && validMobile.test(fields.mobile.value.trim()),
      subject:
        fields.subject &&
        fields.subject.value.trim().length >= 5 &&
        onlyLettersAndSpaces.test(fields.subject.value.trim()),
      message: fields.message && fields.message.value.trim().length >= 10,
    };
    Object.keys(fields).forEach((key) => {
      if (!setFieldError(fields[key], checks[key] ? "" : errors[key]))
        valid = false;
    });
    return valid;
  }

  function validateDonationForm(form) {
    if (!form) return true;
    const fields = {
      name: form.querySelector("#name"),
      mobile: form.querySelector("#mobile"),
      email: form.querySelector("#email"),
      pan: form.querySelector("#pan"),
      amount: form.querySelector("#amount"),
      purpose: form.querySelector("#purpose"),
    };
    const errors = {
      name: "Enter a name using letters and spaces only.",
      mobile: "Enter exactly 10 digits starting with 6, 7, 8, or 9.",
      email: "Enter a valid email address or leave it blank.",
      pan: "PAN must contain 5 letters, 4 digits, and 1 letter.",
      amount: "Enter a valid positive whole-number amount.",
      purpose: "Select where you would like your contribution to help.",
    };
    let valid = true;
    const values = Object.fromEntries(
      Object.entries(fields).map(([key, input]) => [
        key,
        input?.value.trim() || "",
      ]),
    );
    const checks = {
      name: values.name.length >= 3 && onlyLettersAndSpaces.test(values.name),
      mobile: validMobile.test(values.mobile),
      email: !values.email || validEmail.test(values.email),
      pan: !values.pan || /^[A-Z]{5}\d{4}[A-Z]$/.test(values.pan.toUpperCase()),
      amount: positiveInteger.test(values.amount),
      purpose: Boolean(values.purpose),
    };
    Object.keys(fields).forEach((key) => {
      const errorElement = form.querySelector(`#donation-${key}-error`);
      if (
        !setFieldError(
          fields[key],
          checks[key] ? "" : errors[key],
          errorElement,
        )
      )
        valid = false;
    });
    return valid;
  }

  window.validateContactForm = validateContactForm;
  window.validateDonationForm = validateDonationForm;

  const contactForm = document.querySelector("#contactForm");
  if (contactForm) {
    const sanitizeText = (event) => {
      const cleaned = event.target.value.replace(/[^A-Za-z\s]/g, "");
      if (cleaned !== event.target.value) event.target.value = cleaned;
    };
    ["#name", "#subject"].forEach((selector) =>
      contactForm
        .querySelector(selector)
        ?.addEventListener("input", sanitizeText),
    );
    contactForm.querySelector("#mobile")?.addEventListener("input", (event) => {
      event.target.value = event.target.value.replace(/\D/g, "").slice(0, 10);
    });
    ["input", "blur"].forEach((eventName) =>
      contactForm.addEventListener(eventName, () =>
        validateContactForm(contactForm),
      ),
    );
    contactForm.addEventListener("submit", (event) => {
      if (!validateContactForm(contactForm)) event.preventDefault();
    });
  }

  if (donationForm) {
    const sanitizeDonationName = (event) => {
      event.target.value = event.target.value.replace(/[^A-Za-z\s]/g, "");
    };
    donationForm
      .querySelector("#name")
      ?.addEventListener("input", sanitizeDonationName);
    donationForm
      .querySelector("#mobile")
      ?.addEventListener("input", (event) => {
        event.target.value = event.target.value.replace(/\D/g, "").slice(0, 10);
      });
    donationForm
      .querySelector("#amount")
      ?.addEventListener("input", (event) => {
        event.target.value = event.target.value.replace(/\D/g, "");
      });
    donationForm
      .querySelector("#custom-amount")
      ?.addEventListener("input", (event) => {
        event.target.value = event.target.value.replace(/\D/g, "");
      });
    donationForm.querySelector("#pan")?.addEventListener("input", (event) => {
      event.target.value = event.target.value
        .toUpperCase()
        .replace(/[^A-Z0-9]/g, "")
        .slice(0, 10);
    });
    ["input", "change", "blur"].forEach((eventName) =>
      donationForm.addEventListener(eventName, () =>
        validateDonationForm(donationForm),
      ),
    );
    donationForm.addEventListener("submit", (event) => {
      if (!validateDonationForm(donationForm)) event.preventDefault();
    });
  }
});
