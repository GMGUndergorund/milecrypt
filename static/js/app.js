// MileCrypt JavaScript Application

// Theme Management
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize animations
    initializeAnimations();
});

// Theme Functions
function initializeTheme() {
    const savedTheme = localStorage.getItem('milecrypt-theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('milecrypt-theme', theme);
    
    // Update theme toggle button
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon';
    }
    
    // Update any theme-dependent elements
    updateThemeElements(theme);
}

function updateThemeElements(theme) {
    // Update any elements that need theme-specific styling
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        if (theme === 'dark') {
            card.classList.add('text-light');
        } else {
            card.classList.remove('text-light');
        }
    });
}

// Tooltip Initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form Enhancements
function initializeFormEnhancements() {
    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        autoResizeTextarea(textarea);
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time URL validation
    const urlTextareas = document.querySelectorAll('textarea[name="links"]');
    urlTextareas.forEach(textarea => {
        textarea.addEventListener('blur', validateURLs);
        textarea.addEventListener('input', debounce(validateURLs, 500));
    });
}

function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

function validateURLs(e) {
    const textarea = e.target;
    const lines = textarea.value.split('\n').filter(line => line.trim());
    const urlPattern = /^https?:\/\/[^\s/$.?#].[^\s]*$/i;
    
    let hasInvalidURL = false;
    let validCount = 0;
    
    lines.forEach(line => {
        if (line.trim() && !urlPattern.test(line.trim())) {
            hasInvalidURL = true;
        } else if (line.trim()) {
            validCount++;
        }
    });
    
    // Update validation state
    if (hasInvalidURL) {
        textarea.classList.add('is-invalid');
        textarea.classList.remove('is-valid');
    } else if (validCount > 0) {
        textarea.classList.add('is-valid');
        textarea.classList.remove('is-invalid');
    } else {
        textarea.classList.remove('is-valid', 'is-invalid');
    }
    
    // Update counter if exists
    updateURLCounter(textarea, validCount);
}

function updateURLCounter(textarea, count) {
    let counter = textarea.parentNode.querySelector('.url-counter');
    if (!counter) {
        counter = document.createElement('div');
        counter.className = 'url-counter text-muted small mt-1';
        textarea.parentNode.appendChild(counter);
    }
    
    if (count > 0) {
        counter.textContent = `${count} valid URL${count !== 1 ? 's' : ''} detected`;
        counter.className = 'url-counter text-success small mt-1';
    } else {
        counter.textContent = 'Enter URLs to validate';
        counter.className = 'url-counter text-muted small mt-1';
    }
}

// Animation Functions
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    // Observe cards and other elements
    document.querySelectorAll('.card, .alert').forEach(el => {
        observer.observe(el);
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Copy to Clipboard with Enhanced Feedback
function copyToClipboard(text, button) {
    if (navigator.clipboard && window.isSecureContext) {
        // Use modern clipboard API
        navigator.clipboard.writeText(text).then(
            () => showCopySuccess(button),
            () => fallbackCopyTextToClipboard(text, button)
        );
    } else {
        // Fallback for older browsers
        fallbackCopyTextToClipboard(text, button);
    }
}

function fallbackCopyTextToClipboard(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(button);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showCopyError(button);
    }
    
    document.body.removeChild(textArea);
}

function showCopySuccess(button) {
    if (button) {
        const originalHTML = button.innerHTML;
        const originalClass = button.className;
        
        button.innerHTML = '<i class="bi bi-check"></i> Copied!';
        button.className = button.className.replace('btn-outline-secondary', 'btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.className = originalClass;
        }, 2000);
    }
    
    showToast('Copied to clipboard!', 'success');
}

function showCopyError(button) {
    if (button) {
        const originalHTML = button.innerHTML;
        const originalClass = button.className;
        
        button.innerHTML = '<i class="bi bi-x"></i> Error';
        button.className = button.className.replace('btn-outline-secondary', 'btn-danger');
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.className = originalClass;
        }, 2000);
    }
    
    showToast('Failed to copy to clipboard', 'error');
}

// Toast Notification System
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = getOrCreateToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${getBootstrapColorClass(type)} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-${getToastIcon(type)} me-2"></i>${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bootstrapToast = new bootstrap.Toast(toast, {
        delay: duration
    });
    
    bootstrapToast.show();
    
    toast.addEventListener('hidden.bs.toast', function() {
        toastContainer.removeChild(toast);
    });
}

function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    return container;
}

function getBootstrapColorClass(type) {
    const colorMap = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return colorMap[type] || 'info';
}

function getToastIcon(type) {
    const iconMap = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return iconMap[type] || 'info-circle';
}

// Loading States
function showLoading(button) {
    if (button) {
        button.disabled = true;
        button.classList.add('btn-loading');
        const originalText = button.textContent;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    }
}

function hideLoading(button) {
    if (button) {
        button.disabled = false;
        button.classList.remove('btn-loading');
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.textContent = originalText;
            button.removeAttribute('data-original-text');
        }
    }
}

// Form Submission with Loading States
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton) {
        showLoading(submitButton);
        
        // Re-enable button after a delay if form submission fails
        setTimeout(() => {
            hideLoading(submitButton);
        }, 10000);
    }
});

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search or create
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const createButton = document.querySelector('a[href*="create"]');
        if (createButton) {
            window.location.href = createButton.href;
        }
    }
    
    // Ctrl/Cmd + / to toggle theme
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        toggleTheme();
    }
});

// Enhanced Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showToast('An unexpected error occurred. Please refresh the page.', 'error');
});

// Service Worker Registration (for offline functionality)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(function(error) {
        console.log('ServiceWorker registration failed: ', error);
    });
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    // Clean up any ongoing operations
    document.querySelectorAll('.btn-loading').forEach(button => {
        hideLoading(button);
    });
});

// CSS Animation Classes
const animationCSS = `
.animate-fade-in {
    animation: fadeInUp 0.6s ease-out forwards;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.animate-bounce {
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}
`;

// Inject animation CSS
const style = document.createElement('style');
style.textContent = animationCSS;
document.head.appendChild(style);
