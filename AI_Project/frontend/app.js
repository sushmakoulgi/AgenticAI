const topicInput = document.getElementById("topic");
const researchBtn = document.getElementById("researchBtn");
const errorMsg = document.getElementById("error");
const result = document.getElementById("result");
const resultContent = document.getElementById("resultContent");
const progressBar = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");
const progressLabel = document.getElementById("progressLabel");
const planTasks = document.getElementById("planTasks");
const activityLog = document.getElementById("activityLog");
const reportSection = document.getElementById("reportSection");
const reportContent = document.getElementById("reportContent");

// Must match MAX_STEPS in agent.py; used to estimate progress during research
const MAX_RESEARCH_STEPS = 10;

// The four stages of the agent, in order
const STAGES = ["plan", "research", "verify", "report"];

function stageItem(name) {
    return document.querySelector(`.stage[data-stage="${name}"]`);
}

function resetStages() {
    for (const name of STAGES) {
        const item = stageItem(name);
        item.classList.remove("active", "done", "failed");
        item.querySelector("input").checked = false;
    }
    planTasks.replaceChildren();
    planTasks.hidden = true;
}

// Mark every stage before `name` as done and `name` itself as in progress
function startStage(name) {
    for (const stage of STAGES) {
        if (stage === name) {
            const item = stageItem(stage);
            if (!item.classList.contains("done")) item.classList.add("active");
            return;
        }
        completeStage(stage);
    }
}

function completeStage(name) {
    const item = stageItem(name);
    item.classList.remove("active");
    item.classList.add("done");
    item.querySelector("input").checked = true;
}

function failActiveStage() {
    const active = document.querySelector(".stage.active");
    if (active) {
        active.classList.remove("active");
        active.classList.add("failed");
    }
}

// Progress only ever moves forward
let progress = 0;
function setProgress(percent) {
    progress = Math.max(progress, Math.min(100, Math.round(percent)));
    progressFill.style.width = `${progress}%`;
    progressLabel.textContent = `${progress}%`;
    progressBar.setAttribute("aria-valuenow", progress);
}

// Add one line to the activity log; earlier lines are kept
function logActivity(text, detail, kind = "") {
    const item = document.createElement("li");
    if (kind) item.classList.add(kind);

    const time = document.createElement("time");
    time.textContent = new Date().toLocaleTimeString();
    item.append(time);

    const message = document.createElement("span");
    message.className = "activity-message";
    message.textContent = text;
    item.append(message);

    if (detail !== undefined && detail !== null && detail !== "") {
        const extra = document.createElement("span");
        extra.className = "activity-detail";
        extra.textContent = detail;
        item.append(extra);
    }

    // Keep the newest line in view without scrolling the whole page
    activityLog.append(item);
    activityLog.scrollTop = activityLog.scrollHeight;
}

// Update the stages, progress bar and log for one event from the agent
function handleEvent(event) {
    const type = (event.type || "").toLowerCase();
    const message = (event.message || "").trim();

    switch (type) {
        case "plan":
            completeStage("plan");
            startStage("research");
            setProgress(25);
            for (const task of event.output || []) {
                const li = document.createElement("li");
                li.textContent = task;
                planTasks.append(li);
            }
            planTasks.hidden = false;
            logActivity("Research plan is ready", `${(event.output || []).length} tasks`, "done");
            resultContent.textContent = "Researching the planned tasks...";
            break;

        case "research step": {
            const step = Number(String(event.output).match(/\d+/)?.[0]);
            if (!Number.isNaN(step) && /^step \d+$/i.test(String(event.output))) {
                // Start of a research step
                setProgress(25 + (Math.min(step, MAX_RESEARCH_STEPS) / MAX_RESEARCH_STEPS) * 45);
                logActivity(`Research step ${step}`, "Asking the research agent what to do next");
                resultContent.textContent = `Research step ${step} of up to ${MAX_RESEARCH_STEPS}...`;
            } else {
                // The agent made no tool call, so research is finished
                completeStage("research");
                startStage("verify");
                setProgress(75);
                logActivity("Research finished", event.output, "done");
            }
            break;
        }

        case "tool call step":
            logActivity("Calling tool", event.output);
            break;

        case "tool call complete":
            logActivity("Tool finished", event.output, "done");
            break;

        case "verification step":
        case "stopping due to max steps":
            completeStage("research");
            startStage("verify");
            setProgress(75);
            logActivity(type === "verification step" ? "Fetching verified notes" : "Stopped at the step limit", event.output);
            resultContent.textContent = "Verifying the findings...";
            break;

        case "verification":
            completeStage("verify");
            startStage("report");
            setProgress(85);
            logActivity("Findings verified", `${event.output} verified notes`, "done");
            resultContent.textContent = "Writing the report...";
            break;

        case "report":
            completeStage("report");
            setProgress(100);
            logActivity("Report is complete", null, "done");
            break;

        default:
            logActivity(message || event.type || "Update", event.output);
    }
}

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

    // Reset the result card for a new run
    researchBtn.disabled = true;
    researchBtn.textContent = "Researching...";
    result.classList.remove("failed");
    progress = 0;
    setProgress(0);
    resetStages();
    activityLog.replaceChildren();
    reportSection.hidden = true;
    reportContent.textContent = "";
    resultContent.textContent = "Planning the research. This can take a minute...";
    result.hidden = false;

    startStage("plan");
    setProgress(5);
    logActivity("Research started", topic);

    try {
        const res = await fetch("/research", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic: topic }),
        });

        // Errors before the stream starts (e.g. empty topic) come back as normal JSON
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.detail || `Request failed (${res.status})`);
        }

        // The server streams events as "data:{json}\n\n" while the agent works
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let report = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            const messages = buffer.split("\n\n");
            buffer = messages.pop();

            for (const message of messages) {
                if (!message.startsWith("data:")) continue;
                const event = JSON.parse(message.slice("data:".length));

                if (event.error) throw new Error(event.error);
                if (event.result !== undefined) {
                    report = event.result;
                } else {
                    handleEvent(event);
                }
            }
        }

        if (report === null) {
            throw new Error("The research stream ended without a report");
        }

        // Make sure everything is ticked even if an event was missed
        for (const name of STAGES) completeStage(name);
        setProgress(100);
        resultContent.textContent = "Research complete.";

        // The report is plain text, so show it as text
        reportContent.textContent = report;
        reportSection.hidden = false;
        reportSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) {
        result.classList.add("failed");
        failActiveStage();
        resultContent.textContent = `Error: ${err.message}`;
        logActivity("Research failed", err.message, "failed");
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
