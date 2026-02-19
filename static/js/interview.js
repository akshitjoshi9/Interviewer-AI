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

    const interviewId = localStorage.getItem("interview_id");
    console.log("Interview ID:", interviewId);

    if (!interviewId) {
        statusEl.textContent = "Interview session not found.";
        return;
    }

    const res = await fetch(`/api/interview/question/audio/${interviewId}`);

    console.log("Response status:", res.status);
    console.log("Content-Type:", res.headers.get("content-type"));

    // ✅ INTERVIEW COMPLETED
    if (res.headers.get("content-type")?.includes("application/json")) {
        statusEl.innerHTML = `
            <div style="text-align:center">
                <p style="margin-bottom:16px;">
                    <strong>Interview completed</strong>
                </p>
                <button id="viewResultBtn" class="start-btn">
                    📊 View Interview Results
                </button>
            </div>
        `;

        stream?.getTracks().forEach(t => t.stop());

        const btn = document.getElementById("viewResultBtn");
        if (btn) {
            btn.onclick = () => {
                const interviewId = localStorage.getItem("interview_id");
                window.location.href = `/interview/result/${interviewId}`;
            };
        }

        return; // VERY IMPORTANT
    }

    // PLAY QUESTION AUDIO
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

        const interviewId = localStorage.getItem("interview_id");

        await fetch(`/api/interview/answer/${interviewId}`, {
            method: "POST",
            body: formData
        });

        setTimeout(speakQuestion, 800);
    };
};

setTimeout(speakQuestion, 1000);
