document.addEventListener("DOMContentLoaded", () => {
    const timeDisplay = document.getElementById("time-display");
    const dateDisplay = document.getElementById("date-display");

    if (timeDisplay && dateDisplay) {
        function updateTime() {
            const now = new Date();
            const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            dateDisplay.textContent = now.toLocaleDateString(undefined, dateOptions);
            timeDisplay.textContent = now.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }
        setInterval(updateTime, 1000);
        updateTime();
    }

    const messages = document.querySelectorAll(".msg");
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = "opacity 0.5s";
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        }, 4000);
    });
});
