let socket = null;
let recognition = null;
let isSpeaking = false;

function startChat() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(() => {
            connectSocket();
        })
        .catch(err => {
            alert("Microphone permission is required.");
            console.error(err);
        });
}

function stopChat() {
    console.log("Stopping chat");

    if (recognition) {
        recognition.onresult = null;
        recognition.onerror = null;
        recognition.stop();
        recognition = null;
    }

    speechSynthesis.cancel();
    isSpeaking = false;

    if (socket) {
        socket.close();
        socket = null;
    }

    document.getElementById("chat-window").innerHTML = "";
}

function connectSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws/chat");

    socket.onopen = () => {
        console.log("WebSocket Connected");
        startListening();
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        log(data.text, "ai");
        speak(data.text);
    };

    socket.onclose = () => {
        console.log("WebSocket Closed");
    };

    socket.onerror = (e) => {
        console.error("WebSocket error", e);
    };
}

function startListening() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        const transcript =
            event.results[event.results.length - 1][0].transcript.trim();

        if (!isSpeaking && transcript.length > 2 && socket) {
            log(transcript, "user");
            socket.send(JSON.stringify({ text: transcript }));
        }
    };

    recognition.onerror = (e) => {
        console.error("Speech error", e);
    };

    recognition.start();
}

function speak(text) {
    if (!recognition) return;

    isSpeaking = true;
    recognition.stop();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";

    utterance.onend = () => {
        isSpeaking = false;
        if (recognition) recognition.start();
    };

    speechSynthesis.speak(utterance);
}

function log(text, sender) {
    const chatWindow = document.getElementById("chat-window");

    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble", sender === "user" ? "user" : "ai");
    bubble.innerText = text;

    chatWindow.appendChild(bubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
