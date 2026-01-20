function startInterview() {
    fetch("/api/start-interview")
        .then(res => res.json())
        .then(data => console.log(data));
}
