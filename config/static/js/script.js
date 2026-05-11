// UZTMK - Asosiy JavaScript Faylı

document.addEventListener('DOMContentLoaded', function() {
    console.log('UZTMK Tizimi yuklandi');

    // Tooltip faollashtirish
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popover faollashtirish
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Alert avtomatik yopish
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            // bsAlert.close(); // Agar avtomatik yopishni xohlasangiz
        }, 5000);
    });
});

// AJAX so'rovlari uchun helper funksiyalar
const API = {
    // GET so'rovi
    get: function(url) {
        return fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => response.json());
    },

    // POST so'rovi
    post: function(url, data) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        }).then(response => response.json());
    },

    // PUT so'rovi
    put: function(url, data) {
        return fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        }).then(response => response.json());
    },

    // DELETE so'rovi
    delete: function(url) {
        return fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => response.json());
    }
};

// CSRF Token olish
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Formatlashtirish funksiyalari
const Utils = {
    // Sanani formatlashtirish
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('uz-UZ', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    // Vaqtni formatlashtirish
    formatTime: function(timeString) {
        const time = new Date(timeString);
        return time.toLocaleTimeString('uz-UZ', {
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Pulni formatlashtirish
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('uz-UZ', {
            style: 'currency',
            currency: 'UZS'
        }).format(amount);
    },

    // Ro'yxat shaklida formatlashtirish
    formatList: function(items) {
        if (items.length === 0) return '';
        if (items.length === 1) return items[0];
        return items.slice(0, -1).join(', ') + ' va ' + items[items.length - 1];
    }
};

// Notification funksiyalari
const Notify = {
    show: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('main .container-lg');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }

        // Avtomatik yopish
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    },

    success: function(message) {
        this.show(message, 'success');
    },

    error: function(message) {
        this.show(message, 'danger');
    },

    warning: function(message) {
        this.show(message, 'warning');
    },

    info: function(message) {
        this.show(message, 'info');
    }
};

// Konsolda xatolarni ko'rsatish
console.log('%c UZTMK Tizimi', 'color: #0d6efd; font-size: 16px; font-weight: bold;');
console.log('%c Qurilmalarni Boshqarish Tizimi', 'color: #6c757d; font-size: 12px;');
