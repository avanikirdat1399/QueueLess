
// Get the logged-in student's details
const accessToken = sessionStorage.getItem("access_token");
const studentName = sessionStorage.getItem("student_name");

// Redirect to login if the student is not logged in
if (!accessToken) {
    window.location.href = "/auth";
}

// Display student's name
document.getElementById("student-name").textContent =
    studentName || "Student";


// Load available services
async function loadServices() {

    const container = document.getElementById("service-container");

    try {
        const response = await fetch("/api/counters");

        if (!response.ok) {
            throw new Error("Unable to load services");
        }

        const services = await response.json();

        container.innerHTML = "";

        services.forEach(service => {

            const card = document.createElement("div");

            card.className =
                "service-card bg-slate-900 border border-slate-800 rounded-xl p-6";

            card.innerHTML = `
                <h3 class="text-xl font-bold mb-3">
                    ${service.service_name}
                </h3>

                <p class="text-slate-400 mb-5">
                    Generate your token for this service.
                </p>

                <button
                    class="service-button"
                    onclick="generateToken(${service.id})">
                    Generate Token
                </button>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        container.textContent = "Unable to load services.";
        console.error(error);
    }
}


// Generate a digital token
async function generateToken(counterId) {

    try {
        const response = await fetch("/api/tokens", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + accessToken
            },

            body: JSON.stringify({
                counter_id: counterId
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "Token generation failed.");
            return;
        }

        document.getElementById("current-token").innerHTML = `
            <div class="mt-5">
                <p class="text-slate-400">Your Token Number</p>

                <h2 class="text-4xl font-bold text-blue-400 mt-2">
                    ${result.token_number}
                </h2>

                <p class="mt-4">
                    Service: ${result.service}
                </p>

                <p class="text-green-400 mt-2">
                    Status: ${result.status}
                </p>
            </div>
        `;

        alert("Your token has been generated!");

    } catch (error) {
        alert("Unable to connect to the server.");
        console.error(error);
    }
}


// Logout
function logout() {
    sessionStorage.clear();
    window.location.href = "/auth";
}


// Load services when dashboard opens
loadServices();


// Load current queue information
async function loadMyToken() {

    const tokenContainer = document.getElementById("current-token");

    try {
        const response = await fetch("/api/my-token", {
            headers: {
                "Authorization": "Bearer " + accessToken
            }
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to load queue details");
        }

        if (!result.token_number) {
            tokenContainer.innerHTML =
                "<p>You don't have an active token yet.</p>";
            return;
        }

        tokenContainer.innerHTML = `
            <div class="mt-5">

                <p class="text-slate-400">Your Token Number</p>

                <h2 class="text-4xl font-bold text-blue-400 mt-2">
                    ${result.token_number}
                </h2>

                <p class="mt-4">
                    Service: ${result.service}
                </p>

                <p class="text-green-400 mt-2">
                    Status: ${result.status}
                </p>

                <button
                    onclick="cancelToken()"
                    class="bg-red-600 hover:bg-red-700 px-5 py-2 rounded-lg mt-5">
                    Cancel Token
                </button>

                <div class="grid grid-cols-2 gap-4 mt-6">

                    <div class="bg-slate-800 p-4 rounded-lg">
                        <p class="text-slate-400 text-sm">
                            People Ahead
                        </p>
                        <h3 class="text-2xl font-bold mt-2">
                            ${result.people_ahead}
                        </h3>
                    </div>

                    <div class="bg-slate-800 p-4 rounded-lg">
                        <p class="text-slate-400 text-sm">
                            Estimated Wait
                        </p>
                        <h3 class="text-2xl font-bold mt-2">
                            ${result.estimated_wait_minutes} min
                        </h3>
                    </div>

                </div>

            </div>
        `;

    } catch (error) {
        console.error(error);
        tokenContainer.textContent = "Unable to load queue information.";
    }
}


// Refresh queue information
loadMyToken();

setInterval(loadMyToken, 10000);


// Cancel the active token
async function cancelToken() {

    const confirmCancel = confirm(
        "Are you sure you want to cancel your token?"
    );

    if (!confirmCancel) {
        return;
    }

    try {
        const response = await fetch("/api/cancel-token", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + accessToken
            }
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "Cancellation failed");
            return;
        }

        alert("Your token has been cancelled!");

        loadMyToken();

    } catch (error) {
        alert("Unable to connect to the server.");
        console.error(error);
    }
}