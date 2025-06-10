/**
 * نظام القائمة التفاعلي - Interactive Menu System
 * يستخدم Alpine.js للتفاعل و Intl API لتنسيق العملات
 */

// إعدادات العملات والتحويل - Currency settings and conversion
const CURRENCY_RATES = {
    'EGP': 1,
    'USD': 0.032,
    'EUR': 0.029,
    'SAR': 0.12,
    'AED': 0.118
};

// دالة تحويل العملات - Currency conversion function
function convertCurrency(amount, fromCurrency, toCurrency) {
    if (fromCurrency === toCurrency) return amount;

    // تحويل إلى الجنيه المصري أولاً ثم إلى العملة المطلوبة
    // Convert to EGP first, then to target currency
    const egpAmount = amount / CURRENCY_RATES[fromCurrency];
    return egpAmount * CURRENCY_RATES[toCurrency];
}

// دالة تنسيق الأسعار - Price formatting function
function formatPrice(price, currency, targetCurrency, locale = 'ar-EG') {
    const convertedPrice = convertCurrency(parseFloat(price), currency, targetCurrency);

    try {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: targetCurrency,
            minimumFractionDigits: targetCurrency === 'EGP' ? 0 : 2,
            maximumFractionDigits: 2
        }).format(convertedPrice);
    } catch (error) {
        // Fallback if currency is not supported
        return `${convertedPrice.toFixed(2)} ${targetCurrency}`;
    }
}

// دالة البحث المتقدم - Advanced search function
function searchInText(text, query, lang = 'ar') {
    if (!text || !query) return false;

    const normalizedText = text.toLowerCase().trim();
    const normalizedQuery = query.toLowerCase().trim();

    // البحث العادي - Normal search
    if (normalizedText.includes(normalizedQuery)) return true;

    // البحث بالكلمات المفردة - Word-by-word search
    const queryWords = normalizedQuery.split(/\s+/);
    return queryWords.every(word => normalizedText.includes(word));
}

// دالة تحميل البيانات مع التخزين المؤقت - Data loading with caching
class MenuDataManager {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    async fetchWithCache(url, cacheKey) {
        const cached = this.cache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });

            return data;
        } catch (error) {
            console.error('Fetch error:', error);
            // Return cached data if available, even if expired
            return cached ? cached.data : null;
        }
    }

    async getMenu(lang = 'ar') {
        return this.fetchWithCache(`/api/menu?lang=${lang}`, `menu_${lang}`);
    }

    async searchProducts(query, lang = 'ar') {
        if (!query.trim()) return { success: true, data: [] };
        return this.fetchWithCache(
            `/api/search?q=${encodeURIComponent(query)}&lang=${lang}`,
            `search_${query}_${lang}`
        );
    }

    async getSettings() {
        return this.fetchWithCache('/api/settings', 'settings');
    }
}

// مثيل مدير البيانات - Data manager instance
const dataManager = new MenuDataManager();

// دالة مساعدة للرسوم المتحركة - Animation helper function
function animateElement(element, animationClass, duration = 500) {
    return new Promise(resolve => {
        element.classList.add(animationClass);
        setTimeout(() => {
            element.classList.remove(animationClass);
            resolve();
        }, duration);
    });
}

// دالة تحسين الصور - Image optimization function
function optimizeImageUrl(base64Url, maxWidth = 400) {
    if (!base64Url || !base64Url.startsWith('data:image/')) {
        return '/static/images/placeholder.jpg';
    }

    // في التطبيق الحقيقي، يمكن تحسين الصور هنا
    // In real app, could optimize images here
    return base64Url;
}

// دالة التحقق من دعم الميزات - Feature support detection
function checkFeatureSupport() {
    return {
        intl: typeof Intl !== 'undefined',
        fetch: typeof fetch !== 'undefined',
        alpineJs: typeof Alpine !== 'undefined',
        webp: (() => {
            const canvas = document.createElement('canvas');
            return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
        })()
    };
}

// تهيئة النظام عند تحميل الصفحة - System initialization on page load
document.addEventListener('DOMContentLoaded', function() {
    const features = checkFeatureSupport();

    if (!features.fetch) {
        console.warn('Fetch API not supported, menu may not work properly');
    }

    if (!features.intl) {
        console.warn('Intl API not supported, currency formatting may be limited');
    }

    // إضافة معالجات الأحداث العامة - Add global event handlers
    document.addEventListener('keydown', function(e) {
        // إغلاق النوافذ المنبثقة بالضغط على Escape
        // Close modals with Escape key
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('[x-show="showModal"]');
            modals.forEach(modal => {
                if (modal.style.display !== 'none') {
                    // Trigger Alpine.js close function
                    const alpineData = Alpine.$data(modal);
                    if (alpineData && typeof alpineData.closeModal === 'function') {
                        alpineData.closeModal();
                    }
                }
            });
        }
    });

    // تحسين الأداء للصور - Performance optimization for images
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
});

// إدارة السلة - Cart Management
class CartManager {
    constructor() {
        this.updateCartDisplay();
    }

    // تحديث عرض السلة - Update cart display
    updateCartDisplay() {
        this.getCartCount().then(count => {
            const cartCountElement = document.getElementById('cart-count');
            if (cartCountElement) {
                cartCountElement.textContent = count;
                cartCountElement.style.display = count > 0 ? 'flex' : 'none';
            }
        });
    }

    // الحصول على عدد عناصر السلة - Get cart items count
    async getCartCount() {
        try {
            const response = await fetch('/api/cart/count');
            if (response.ok) {
                const data = await response.json();
                return data.count || 0;
            }
        } catch (error) {
            console.error('Error getting cart count:', error);
        }
        return 0;
    }

    // إضافة منتج للسلة - Add product to cart
    async addToCart(productId, quantity = 1) {
        try {
            const formData = new FormData();
            formData.append('quantity', quantity);

            const response = await fetch(`/cart/add/${productId}`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.updateCartDisplay();
                this.showCartNotification('تم إضافة المنتج للسلة بنجاح');
                return true;
            } else {
                this.showCartNotification('حدث خطأ أثناء إضافة المنتج', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
            this.showCartNotification('حدث خطأ أثناء إضافة المنتج', 'error');
            return false;
        }
    }

    // عرض إشعار السلة - Show cart notification
    showCartNotification(message, type = 'success') {
        // إنشاء عنصر الإشعار - Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-20 right-4 z-50 max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden transform transition-all duration-300 translate-x-full`;

        const bgColor = type === 'success' ? 'bg-green-50' : 'bg-red-50';
        const textColor = type === 'success' ? 'text-green-800' : 'text-red-800';
        const iconClass = type === 'success' ? 'fa-check-circle text-green-400' : 'fa-exclamation-circle text-red-400';

        notification.innerHTML = `
            <div class="p-4 ${bgColor}">
                <div class="flex items-start">
                    <div class="flex-shrink-0">
                        <i class="fas ${iconClass}"></i>
                    </div>
                    <div class="mr-3 w-0 flex-1 pt-0.5">
                        <p class="text-sm font-medium ${textColor}">${message}</p>
                    </div>
                    <div class="ml-4 flex-shrink-0 flex">
                        <button onclick="this.parentElement.parentElement.parentElement.parentElement.remove()"
                                class="bg-transparent rounded-md inline-flex ${textColor} hover:opacity-75">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // إظهار الإشعار - Show notification
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        // إخفاء الإشعار تلقائياً - Auto hide notification
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// مثيل مدير السلة - Cart manager instance
const cartManager = new CartManager();

// تصدير الدوال للاستخدام العام - Export functions for global use
window.MenuUtils = {
    formatPrice,
    convertCurrency,
    searchInText,
    optimizeImageUrl,
    dataManager,
    animateElement,
    cartManager
};