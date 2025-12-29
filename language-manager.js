// =============================================
// LANGUAGE MANAGER - Sistema de Multiidioma
// =============================================

class LanguageManager {
    constructor() {
        // Configuración de idiomas soportados
        this.supportedLanguages = [
            { code: 'en', name: 'English', native: 'English', dir: 'ltr' },
            { code: 'es', name: 'Español', native: 'Español', dir: 'ltr' },
            { code: 'zh', name: 'Chinese', native: '中文', dir: 'ltr' },
            { code: 'hi', name: 'Hindi', native: 'हिन्दी', dir: 'ltr' },
            { code: 'fr', name: 'French', native: 'Français', dir: 'ltr' },
            { code: 'de', name: 'German', native: 'Deutsch', dir: 'ltr' },
            { code: 'ar', name: 'Arabic', native: 'العربية', dir: 'rtl' },
            { code: 'bn', name: 'Bengali', native: 'বাংলা', dir: 'ltr' },
            { code: 'pt', name: 'Portuguese', native: 'Português', dir: 'ltr' },
            { code: 'ru', name: 'Russian', native: 'Русский', dir: 'ltr' },
            { code: 'ur', name: 'Urdu', native: 'اردو', dir: 'rtl' }
        ];

        this.currentLanguage = 'en'; // Idioma por defecto
        this.translations = {};
        this.isInitialized = false;
    }

    // =============================================
    // INICIALIZACIÓN
    // =============================================

    async init() {
        if (this.isInitialized) return;

        // 1. Obtener idioma guardado o detectar
        await this.detectAndSetLanguage();

        // 2. Cargar traducciones del idioma actual
        await this.loadLanguage(this.currentLanguage);

        // 3. Aplicar traducciones a la página actual
        this.applyTranslations();

        // 4. Configurar el selector de idioma si existe
        this.setupLanguageSelector();

        // 5. Aplicar estilos RTL si es necesario
        this.applyTextDirection();

        this.isInitialized = true;
        console.log(`Language manager initialized: ${this.currentLanguage}`);
    }

    async detectAndSetLanguage() {
        // Prioridad 1: Idioma guardado en localStorage
        const savedLang = localStorage.getItem('mayusc_language');

        // Prioridad 2: Idioma del navegador (solo si está soportado)
        const browserLang = navigator.language.split('-')[0];

        // Prioridad 3: Idioma por defecto (en)
        if (savedLang && this.isLanguageSupported(savedLang)) {
            this.currentLanguage = savedLang;
        } else if (this.isLanguageSupported(browserLang)) {
            this.currentLanguage = browserLang;
        } else {
            this.currentLanguage = 'en';
        }

        // Guardar en localStorage
        localStorage.setItem('mayusc_language', this.currentLanguage);
    }

    isLanguageSupported(langCode) {
        return this.supportedLanguages.some(lang => lang.code === langCode);
    }

    // =============================================
    // CARGA DE TRADUCCIONES
    // =============================================

    async loadLanguage(langCode) {
        try {
            const response = await fetch(`translations/${langCode}.json`);

            if (!response.ok) {
                throw new Error(`Failed to load ${langCode}.json`);
            }

            this.translations = await response.json();
            console.log(`Loaded language: ${langCode}`);

        } catch (error) {
            console.error(`Error loading language ${langCode}:`, error);

            // Intentar cargar inglés como fallback
            if (langCode !== 'en') {
                console.log('Trying to load English as fallback...');
                await this.loadLanguage('en');
                this.currentLanguage = 'en';
            }
        }
    }

    // =============================================
    // APLICACIÓN DE TRADUCCIONES
    // =============================================

    applyTranslations() {
        // Actualizar todos los elementos con data-i18n
        // 1. Process elements with data-i18n (text content and attributes)
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);

            if (translation) {
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.placeholder = translation;
                } else if (element.hasAttribute('data-i18n-attr')) {
                    const attr = element.getAttribute('data-i18n-attr');
                    element.setAttribute(attr, translation);
                } else {
                    element.textContent = translation;
                }
            }
        });

        // 2. Process elements with data-i18n-html (HTML content)
        document.querySelectorAll('[data-i18n-html]').forEach(element => {
            const key = element.getAttribute('data-i18n-html');
            const translation = this.getTranslation(key);

            if (translation) {
                element.innerHTML = translation.replace(/\n/g, '<br>');
            }
        });

        // Actualizar el atributo lang del HTML
        document.documentElement.lang = this.currentLanguage;

        // Actualizar el título de la página si existe
        const pageTitle = this.getTranslation('pages.' + this.getCurrentPage() + '.title');
        if (pageTitle && document.title !== 'Credits') {
            document.title = pageTitle;
        }
    }

    getTranslation(key) {
        // Buscar la traducción usando notación de puntos (ej: "pages.home.title")
        const keys = key.split('.');
        let result = this.translations;

        for (const k of keys) {
            if (result && typeof result === 'object' && k in result) {
                result = result[k];
            } else {
                console.warn(`Translation key not found: ${key}`);
                return null;
            }
        }

        return result;
    }

    getCurrentPage() {
        // Determinar la página actual basada en la URL
        const path = window.location.pathname;
        if (path.includes('index.html') || path.endsWith('/')) return 'home';
        if (path.includes('text_tools.html')) return 'textTools';
        if (path.includes('settings.html')) return 'settings';
        if (path.includes('Credits.html')) return 'credits';
        return 'home';
    }

    // =============================================
    // SELECTOR DE IDIOMA
    // =============================================

    setupLanguageSelector() {
        const selector = document.getElementById('language-selector');

        if (selector) {
            // Limpiar opciones existentes para evitar duplicados
            selector.innerHTML = '';

            // Llenar el selector con idiomas
            this.supportedLanguages.forEach(lang => {
                const option = document.createElement('option');
                option.value = lang.code;
                option.textContent = lang.native;
                selector.appendChild(option);
            });

            // Establecer el idioma actual
            selector.value = this.currentLanguage;

            // Escuchar cambios
            selector.addEventListener('change', (e) => {
                this.changeLanguage(e.target.value);
            });
        }
    }

    // =============================================
    // CAMBIO DE IDIOMA
    // =============================================

    async changeLanguage(langCode) {
        if (!this.isLanguageSupported(langCode)) {
            console.error(`Language not supported: ${langCode}`);
            return;
        }

        // Mostrar indicador de carga
        this.showLoadingIndicator();

        // Cambiar idioma
        this.currentLanguage = langCode;
        localStorage.setItem('mayusc_language', langCode);

        // Cargar nuevas traducciones
        await this.loadLanguage(langCode);

        // Aplicar traducciones
        this.applyTranslations();
        this.applyTextDirection();

        // Ocultar indicador de carga
        this.hideLoadingIndicator();

        console.log(`Language changed to: ${langCode}`);
    }

    showLoadingIndicator() {
        // Puedes personalizar esto si quieres
        console.log('Changing language...');
    }

    hideLoadingIndicator() {
        // Puedes personalizar esto si quieres
        console.log('Language changed successfully');
    }

    // =============================================
    // DIRECCIÓN DEL TEXTO (RTL/LTR)
    // =============================================

    applyTextDirection() {
        const currentLang = this.supportedLanguages.find(lang => lang.code === this.currentLanguage);

        if (currentLang) {
            document.documentElement.dir = currentLang.dir;

            // Añadir clase CSS para RTL si es necesario
            if (currentLang.dir === 'rtl') {
                document.documentElement.classList.add('rtl-layout');
            } else {
                document.documentElement.classList.remove('rtl-layout');
            }
        }
    }

    // =============================================
    // FUNCIÓN PÚBLICA PARA OBTENER TRADUCCIONES
    // =============================================

    t(key) {
        return this.getTranslation(key) || key;
    }
}

// =============================================
// INSTANCIA GLOBAL
// =============================================

// Crear instancia global
window.languageManager = new LanguageManager();

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.languageManager.init();
});

// También exportar para módulos si es necesario
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageManager;
}