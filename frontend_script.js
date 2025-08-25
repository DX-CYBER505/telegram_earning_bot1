const BACKEND_URL = "https://pochi-backend.onrender.com"; // Update after backend deployment

async function login() {
    const userId = document.getElementById("userId").value;
    if (!userId) {
        alert("Please enter your Telegram User ID");
        return;
    }

    try {
        const response = await fetch(`${BACKEND_URL}/user?user_id=${userId}`);
        const data = await response.json();
        if (data.status === "success") {
            document.getElementById("login").style.display = "none";
            document.getElementById("dashboard").style.display = "block";
            document.getElementById("userName").innerText = `User ${userId}`;
            document.getElementById("points").innerText = data.points;
            document.getElementById("referrals").innerText = data.referrals;
            document.getElementById("usdt").innerText = (data.points * 0.0005).toFixed(4);
            document.getElementById("leaderboard").innerText = data.leaderboard;
        } else {
            alert("User not found. Please start the bot on Telegram first.");
        }
    } catch (error) {
        alert("Error connecting to backend. Try again later.");
    }
}

async function refresh() {
    const userId = document.getElementById("userId").value;
    login();
}