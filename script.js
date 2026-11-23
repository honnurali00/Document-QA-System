
// ===== GET HTML ELEMENTS =====

const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");
const chatMessages = document.getElementById("chatMessages");

const knowledgeGrid = document.getElementById("knowledgeGrid");

const evaluationResults = document.getElementById("evaluationResults");

const reasoningOutput = document.getElementById("reasoningOutput");


// ===== DISPLAY CHAT MESSAGES =====

function displayMessage(message, type) {

    const messageElement = document.createElement("div");

    messageElement.classList.add("message");

    if (type === "user") {
        messageElement.classList.add("user-message");
    } else {
        messageElement.classList.add("assistant-message");
    }

    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// ===== ASK QUESTION =====

async function askQuestion() {

    const question = questionInput.value.trim();

    if (question === "") {
        alert("Please enter a question.");
        return;
    }

    displayMessage(question, "user");

    questionInput.value = "";

    askButton.disabled = true;
    askButton.textContent = "Thinking...";

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        if (!response.ok) {
            throw new Error("Server returned an error.");
        }

        const data = await response.json();

        displayMessage(data.answer, "assistant");

        reasoningOutput.textContent =
            data.reasoning || "No reasoning trace available.";

    } catch (error) {

        displayMessage(
            "Sorry, something went wrong. Please try again.",
            "assistant"
        );

        console.error(error);

    } finally {

        askButton.disabled = false;
        askButton.textContent = "Ask Question";

    }
}


// ===== QUICK QUESTIONS =====

function quickQuestion(question) {

    questionInput.value = question;

    askQuestion();

}


// ===== LOAD KNOWLEDGE BASE =====

async function loadKnowledge() {

    try {

        const response = await fetch("/knowledge");

        if (!response.ok) {
            throw new Error("Could not load Knowledge Base.");
        }

        const knowledge = await response.json();

        knowledgeGrid.replaceChildren();

        for (const key in knowledge) {

            const item = document.createElement("div");

            item.classList.add("knowledge-item");

            const heading = document.createElement("h3");

            heading.textContent = key;

            const value = document.createElement("p");

            value.textContent = knowledge[key];

            item.appendChild(heading);

            item.appendChild(value);

            knowledgeGrid.appendChild(item);

        }

    } catch (error) {

        knowledgeGrid.textContent =
            "Unable to load Knowledge Base.";

        console.error(error);

    }

}


// ===== RUN SYSTEM EVALUATION =====

async function runEvaluation() {

    evaluationResults.textContent = "Running evaluation...";

    try {

        const response = await fetch("/evaluate");

        if (!response.ok) {
            throw new Error("Evaluation failed.");
        }

        const data = await response.json();

        evaluationResults.textContent = data.results;

    } catch (error) {

        evaluationResults.textContent =
            "Unable to run evaluation. Please try again.";

        console.error(error);

    }

}


// ===== BUTTON EVENTS =====

askButton.addEventListener("click", askQuestion);


// Allow Enter key to ask a question

questionInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        askQuestion();
    }

});


// ===== LOAD KNOWLEDGE BASE WHEN PAGE OPENS =====

loadKnowledge();
