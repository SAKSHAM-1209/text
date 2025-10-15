(() => {
    console.log("✅ schedule-call.js loaded");

    const form = document.getElementById('scheduleForm');
    const timeSlot = document.getElementById('timeSlot');
    const feedback = document.getElementById('feedback');
    const submitBtn = form?.querySelector('button[type="submit"]');

    if (!form) {
        console.error("❌ scheduleForm not found");
        return;
    }

    // ===== Generate time slots =====
    const generateTimeSlots = () => {
        timeSlot.innerHTML = '';
        const defaultOpt = document.createElement('option');
        defaultOpt.value = '';
        defaultOpt.textContent = 'Select a time';
        timeSlot.appendChild(defaultOpt);

        for (let h = 9; h <= 17; h++) {
            [0, 30].forEach(min => {
                if (h === 17 && min === 30) return;
                const hh = String(h).padStart(2, '0');
                const mm = String(min).padStart(2, '0');
                const opt = document.createElement('option');
                opt.value = `${hh}:${mm}`;
                opt.textContent = `${hh}:${mm}`;
                timeSlot.appendChild(opt);
            });
        }
    };
    generateTimeSlots();

    // ===== Feedback =====
    const showError = msg => {
        feedback.classList.remove('hidden');
        feedback.style.background = '#fff5f5';
        feedback.style.color = '#7f1d1d';
        feedback.style.border = '1px solid #fecaca';
        feedback.textContent = msg;
    };

    const showSuccess = msg => {
        feedback.classList.remove('hidden');
        feedback.style.background = '#f0fdf4';
        feedback.style.color = '#065f46';
        feedback.style.border = '1px solid #bbf7d0';
        feedback.textContent = msg;
        setTimeout(() => feedback.classList.add('hidden'), 5000);
    };

    const clearFeedback = () => {
        feedback.classList.add('hidden');
        feedback.textContent = '';
    };

    // ===== Form submit =====
    form.addEventListener('submit', e => {
        e.preventDefault();
        clearFeedback();

        // ===== Validation =====
        const nameField = document.getElementById('id_name');
        const emailField = document.getElementById('id_email');
        const phoneField = document.getElementById('id_phone');
        const dateField = document.getElementById('id_date');
        const reasonField = document.getElementById('reason');
        const notesField = document.getElementById('id_notes');

        if (!nameField.value.trim()) return showError('Please enter your name.');
        if (!/\S+@\S+\.\S+/.test(emailField.value.trim())) return showError('Please enter a valid email.');
        if (phoneField.value.trim().length < 7) return showError('Please enter a valid phone number.');
        if (!dateField.value) return showError('Choose a preferred date.');
        if (!timeSlot.value) return showError('Choose a time slot.');
        if (!reasonField.value) return showError('Please select a reason.');

        const formData = new FormData(form);

        // Disable button during request
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = "Submitting...";
        }

        // ===== AJAX POST =====
        fetch(window.location.href, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: formData
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
            return res.json();
        })
        .then(resp => {
            if (resp.success) {
                showSuccess(resp.message);
                form.reset();
                generateTimeSlots();
            } else {
                let errMsg = 'Please correct the errors.';
                if (resp.error) {
                    try {
                        const errors = JSON.parse(resp.error);
                        errMsg = Object.values(errors)
                            .map(e => e.map(x => x.message).join(', '))
                            .join(' | ');
                    } catch { }
                }
                showError(errMsg);
            }
        })
        .catch(err => {
            console.error("❌ Fetch error:", err);
            showError('Server error. Please try again.');
        })
        .finally(() => {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = "Schedule";
            }
        });
    });
})();
