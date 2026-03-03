const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
  });

  mainWindow.loadURL("http://127.0.0.1:8000");
}

function startBackend() {
  const scriptPath = path.join(__dirname, "../backend/run.py");

  backendProcess = spawn("python", [scriptPath], {
    shell: true,
  });

  backendProcess.stdout.on("data", (data) => {
    console.log(`PYTHON: ${data}`);
  });

  backendProcess.stderr.on("data", (data) => {
    console.error(`PYTHON ERROR: ${data}`);
  });
}

app.whenReady().then(() => {
  startBackend();

  setTimeout(() => {
    createWindow();
  }, 3000);
});

app.on("window-all-closed", () => {
  if (backendProcess) backendProcess.kill();
  if (process.platform !== "darwin") app.quit();
});