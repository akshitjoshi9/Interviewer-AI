const statusEl = document.getElementById("ai-status");
const submitBtn = document.getElementById("submitBtn");

let mediaRecorder;
let audioChunks = [];
let stream;
let micInitialized = false;

function hideSubmit() {
    submitBtn.style.display = "none";
}

function showSubmit() {
    submitBtn.style.display = "inline-block";
    submitBtn.disabled = false;
}

async function startRecording() {
    if (!micInitialized) {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        micInitialized = true;
    }

    audioChunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) audioChunks.push(e.data);
    };

    mediaRecorder.start();
    statusEl.textContent = "Recording your answer...";
    showSubmit();
}

async function speakQuestion() {
    hideSubmit();
    statusEl.textContent = "AI is speaking...";

    const res = await fetch("/api/interview/question/audio");

    if (res.headers.get("content-type")?.includes("application/json")) {
        statusEl.textContent = "Interview completed";
        stream?.getTracks().forEach(t => t.stop());
        return;
    }

    const audioBlob = await res.blob();
    const audio = new Audio(URL.createObjectURL(audioBlob));

    audio.onended = () => {
        startRecording();
    };

    audio.play();
}

submitBtn.onclick = async () => {
    submitBtn.disabled = true;
    statusEl.textContent = "Processing answer...";

    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("file", audioBlob, "answer.webm");

        await fetch("/api/interview/answer", {
            method: "POST",
            body: formData
        });

        setTimeout(speakQuestion, 800);
    };
};

setTimeout(speakQuestion, 1000);

