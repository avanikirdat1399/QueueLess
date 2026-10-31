
// Switch to Login form
function showLogin() {

    document.getElementById("login-form").classList.remove("hidden");
    document.getElementById("register-form").classList.add("hidden");

    document.getElementById("login-tab").className =
        "bg-blue-600 rounded-lg py-2 font-semibold";

    document.getElementById("register-tab").className =
        "text-slate-300 rounded-lg py-2 font-semibold";

    document.getElementById("auth-message").textContent = "";
}


// Switch to Registration form
function showRegister() {

    document.getElementById("register-form").classList.remove("hidden");
    document.getElementById("login-form").classList.add("hidden");

    document.getElementById("register-tab").className =
        "bg-blue-600 rounded-lg py-2 font-semibold";

    document.getElementById("login-tab").className =
        "text-slate-300 rounded-lg py-2 font-semibold";

    document.getElementById("auth-message").textContent = "";
}


// Student Registration
document.getElementById("register-form").addEventListener("submit", async function(event) {

    event.preventDefault();

    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    const message = document.getElementById("auth-message");

    try {

        const response = await fetch("/api/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Registration failed");
        }

        message.textContent = "Account created successfully! Please login.";
        message.className = "text-center text-sm mt-6 text-green-400";

        document.getElementById("register-form").reset();

        showLogin();

        message.textContent = "Account created successfully! Please login.";
        message.className = "text-center text-sm mt-6 text-green-400";

    } catch (error) {

        message.textContent = error.message;
        message.className = "text-center text-sm mt-6 text-red-400";

    }

});


// Student Login
document.getElementById("login-form").addEventListener("submit", async function(event) {

    event.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const message = document.getElementById("auth-message");

    try {

        const response = await fetch("/api/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Login failed");
        }

        // Store access token in browser session
        sessionStorage.setItem("access_token", result.access_token);

        sessionStorage.setItem("student_name", result.user.name);

        window.location.href = "/dashboard";

        message.textContent = "Login successful! Welcome " + result.user.name;

        message.className = "text-center text-sm mt-6 text-green-400";

        console.log("Login successful:", result.user);

    } catch (error) {

        message.textContent = error.message;
        message.className = "text-center text-sm mt-6 text-red-400";

    }

});
