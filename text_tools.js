const input = document.getElementById("inputText");
const output = document.getElementById("outputText");

const lowercaseBtn = document.getElementById("lowercaseBtn");
const uppercaseBtn = document.getElementById("uppercaseBtn");
const corretionBtn = document.getElementById("corretionBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");
const endButtons = document.getElementById("endButtons");

// function to enable/disable buttons
function updateButtonStates() {
    const hasText = input.value.trim().length > 0;
    lowercaseBtn.disabled = !hasText;
    uppercaseBtn.disabled = !hasText;
    corretionBtn.disabled = !hasText;
}

// Initial state
updateButtonStates();

// Listen for input changes
input.addEventListener("input", updateButtonStates);

// lowercase
lowercaseBtn.addEventListener("click", () => {
    output.value = input.value.toLowerCase();
    endButtons.classList.remove("hidden");
});

// UPPERCASE
uppercaseBtn.addEventListener("click", () => {
    output.value = input.value.toUpperCase();
    endButtons.classList.remove("hidden");
});

// AI CORRECTION
corretionBtn.addEventListener("click", async () => {
    const texto = input.value.trim();

    if (!texto) {
        return;
    }

    // Usar traducción para el mensaje de carga
    const correctingMsg = window.languageManager 
        ? window.languageManager.t('pages.textTools.messages.correcting')
        : "Correcting... this may take a moment";
    
    output.value = correctingMsg;
    lowercaseBtn.disabled = true;
    uppercaseBtn.disabled = true;
    corretionBtn.disabled = true;

    try {
        const response = await fetch("https://textcorapi.onrender.com/correct", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: texto })
        });

        const textoCorregido = await response.text();
        output.value = textoCorregido;
        endButtons.classList.remove("hidden");

    } catch (error) {
        // Usar traducción para el mensaje de error
        const errorMsg = window.languageManager
            ? window.languageManager.t('pages.textTools.messages.correctingError')
            : "Error correcting text";
        
        output.value = errorMsg;
        console.error(error);
    } finally {
        updateButtonStates();
    }
});

// CLEAR
clearBtn.addEventListener("click", () => {
    input.value = "";
    output.value = "";
    updateButtonStates();
    endButtons.classList.add("hidden");
});

// COPY
copyBtn.addEventListener("click", () => {
    if (output.value === "") return;

    navigator.clipboard.writeText(output.value);
    
    // Mostrar mensaje de éxito (opcional)
    if (window.languageManager) {
        const successMsg = window.languageManager.t('ui.copySuccess');
        // Puedes mostrar un toast o alerta aquí si quieres
        console.log(successMsg);
    }
});