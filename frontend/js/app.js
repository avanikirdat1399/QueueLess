// Display current year in footer
document.getElementById("year").textContent =
    new Date().getFullYear();


// Service details
const serviceDetails = {
    "Administrative Office": {
        icon: "📄",
        description: "Certificates, bonafide requests and student documents."
    },

    "Fees Counter": {
        icon: "💳",
        description: "Fee payments, receipts and payment-related queries."
    },

    "Student Section": {
        icon: "🎓",
        description: "Academic records, examination and student enquiries."
    }
};


// Fetch services from backend
async function loadServices() {

    const container = document.getElementById("service-container");

    try {

        const response = await fetch("/api/counters");

        if (!response.ok) {
            throw new Error("Unable to fetch services");
        }

        const services = await response.json();

        container.innerHTML = "";

        services.forEach(service => {

            const details = serviceDetails[service.service_name] || {
                icon: "🏢",
                description: "Select this service to join its queue."
            };

            const card = document.createElement("div");
            card.className = "service-card";

            const icon = document.createElement("div");
            icon.className = "text-4xl mb-5";
            icon.textContent = details.icon;

            const heading = document.createElement("h3");
            heading.className = "text-xl font-bold";
            heading.textContent = service.service_name;

            const description = document.createElement("p");
            description.className = "text-slate-400 mt-3";
            description.textContent = details.description;

            const button = document.createElement("button");
            button.className = "service-button";
            button.textContent = "Select Service →";

            button.addEventListener("click", function () {
                selectService(service.service_name);
            });

            card.appendChild(icon);
            card.appendChild(heading);
            card.appendChild(description);
            card.appendChild(button);

            container.appendChild(card);

        });

        console.log("Services loaded:", services);

    } catch (error) {

        console.error("Error loading services:", error);

        container.textContent =
            "Unable to load services. Please try again.";

    }
}


// Handle service selection
function selectService(serviceName) {

    // Save the selected service
    sessionStorage.setItem("selected_service", serviceName);

    // Open student login
    window.location.href = "/auth";
}


// Load services when page opens
loadServices();

