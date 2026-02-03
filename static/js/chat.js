document.addEventListener("DOMContentLoaded", () => {

    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("user-input");
    const toggle = document.getElementById("theme-toggle");
    const welcome = document.getElementById("welcome");

    /* DARK MODE */
    toggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        toggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
    });

    /* SEND MESSAGE */
    window.sendMessage = function () {
        const message = input.value.trim();
        if (!message) return;

        // Remove welcome on first message
        if (welcome) {
            welcome.remove();
        }

        addMessage(message, "user");
        input.value = "";
        showTyping();

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        })
            .then(res => res.json())
            .then(data => {
                removeTyping();
                addMessage(data.response, "bot");
            })
            .catch(() => {
                removeTyping();
                addMessage("Something went wrong. Please try again.", "bot");
            });
    };

    /* ENTER KEY */
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    /* QUICK FAQ BUTTONS */
    window.quickSend = function (text) {
        input.value = text;
        sendMessage();
    };

    /* CLEAR CHAT */
    window.clearChat = function () {
        chatBox.innerHTML = `
            <div class="welcome" id="welcome">
                <h2>Hey User 👋</h2>
                <p>How may I help you today?</p>
            </div>
        `;
    };

    /* HELPERS */
    function addMessage(text, cls) {
        const div = document.createElement("div");
        div.className = cls;
        div.innerText = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTyping() {
        const typing = document.createElement("div");
        typing.className = "typing bot";
        typing.id = "typing";
        typing.innerHTML = "<span></span><span></span><span></span>";
        chatBox.appendChild(typing);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTyping() {
        const typing = document.getElementById("typing");
        if (typing) typing.remove();
    }

});
