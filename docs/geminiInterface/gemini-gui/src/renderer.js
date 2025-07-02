const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', async () => {
    const prompt = userInput.value.trim();
    if (!prompt) return;

    // Exibe a pergunta do usuário
    chatContainer.innerHTML += `<div><strong>Você:</strong> ${prompt}</div>`;
    userInput.value = '';

    // Chama o Gemini via Electron
    try {
        const resposta = await window.electronAPI.sendPrompt(prompt);
        chatContainer.innerHTML += `<div><strong>Gemini:</strong> ${resposta}</div>`;
    } catch (error) {
        chatContainer.innerHTML += `<div style="color: red;">Erro: ${error.message}</div>`;
    }
});