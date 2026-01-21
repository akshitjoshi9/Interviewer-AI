const questionEl = document.getElementById("ai-question");
const statusEl = document.getElementById("ai-status");

function speakQuestion(text) {
    // Update UI
    questionEl.textContent = text;
    questionEl.classList.add("speaking");
    statusEl.textContent = "AI is speaking...";

    // Simulate AI speaking time
    setTimeout(() => {
        questionEl.classList.remove("speaking");
        statusEl.textContent = "Your turn to answer";
    }, 4000);
}

// Example first question
setTimeout(() => {
    speakQuestion("Please introduce yourself and describe your current role.");
}, 1500);
