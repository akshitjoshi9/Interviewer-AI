async function startInterview() {
    const jd = document.getElementById("jdInput").value.trim();

    if (!jd) {
        alert("Please paste Job Description");
        return;
    }

    await fetch("/api/interview/init", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jd })
    });

    window.location.href = "/interview";
}
