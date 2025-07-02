const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Configuração do Gemini
const genAI = new GoogleGenerativeAI('SUA_API_KEY'); // Substitua pela sua chave

async function getGeminiResponse(prompt) {
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });
    const result = await model.generateContent(prompt);
    return result.response.text();
}

// Criar janela Electron
function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            sandbox: true,
        },
    });

    win.loadFile('index.html');
}

app.whenReady().then(() => {
    createWindow();

    // Comunicação entre frontend e backend
    ipcMain.handle('gemini-query', async (event, prompt) => {
        return await getGeminiResponse(prompt);
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});