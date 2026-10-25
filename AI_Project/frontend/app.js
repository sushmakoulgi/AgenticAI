const topicInput = document.getElementById("topic");
const researchBtn = document.getElementById("researchBtn");
const errorMsg = document.getElementById("error");
const result = document.getElementById("result");
const resultContent = document.getElementById("resultContent");
const reportContent = document.getElementById("reportContent");

researchBtn.addEventListener("click", async () => {
    const topic = topicInput.value.trim();

    if (topic === "") {
        errorMsg.hidden = false;
        topicInput.classList.add("invalid");
        result.hidden = true;
        topicInput.focus();
        return;
    }

    errorMsg.hidden = true;
    topicInput.classList.remove("invalid");

    // Show a loading state while the agent works
    researchBtn.disabled = true;
    researchBtn.textContent = "Researching...";
    result.classList.remove("failed");
    reportContent.hidden = true;
    reportContent.innerHTML = "";
    resultContent.hidden = false;
    resultContent.textContent = "Planning, researching and writing your report. This can take a minute...";
    result.hidden = false;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ request: topic }),
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || `Request failed (${res.status})`);
        }

        // The response is an HTML report built by the server (all text is escaped there)
        resultContent.hidden = true;
        reportContent.innerHTML = data.response;
        reportContent.hidden = false;
    } catch (err) {
        result.classList.add("failed");
        resultContent.textContent = `Error: ${err.message}`;
    } finally {
        researchBtn.disabled = false;
        researchBtn.textContent = "Research";
    }
});

// Clear the error as soon as the user starts typing
topicInput.addEventListener("input", () => {
    if (topicInput.value.trim() !== "") {
        errorMsg.hidden = true;
        topicInput.classList.remove("invalid");
    }
});
