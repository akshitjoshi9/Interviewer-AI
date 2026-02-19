async function startInterview() {
    const jd = document.getElementById("jdInput").value.trim();

    if (!jd) {
        alert("Please paste Job Description");
        return;
    }

    const res = await fetch("/api/interview/init", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jd })
    });

    const data = await res.json();

    if (data.interview_id) {
        localStorage.setItem("interview_id", data.interview_id);
    }

    window.location.href = "/interview";
}
