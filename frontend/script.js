const BACKEND_URL = "http://<your-backend-container-FQDN>:8000";

document.getElementById("dreamJobForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const name = document.getElementById("name").value;
    const job = document.getElementById("job").value;

    try {
        const response = await fetch(`${BACKEND_URL}/submit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, job })
        });

        if (response.ok) {
            // Show success message
            const successMessage = document.getElementById("successMessage");
            successMessage.classList.add("show");
            
            // Clear form
            event.target.reset();
            
            // Hide success message after 5 seconds
            setTimeout(() => {
                successMessage.classList.remove("show");
            }, 5000);
        }
    } catch (error) {
        console.error("Error submitting dream job:", error);
        alert("There was an error submitting your dream job. Please try again.");
    }
});

// Fetch and display dream jobs
async function fetchJobs() {
    try {
        const response = await fetch(`${BACKEND_URL}/jobs`);
        const jobs = await response.json();

        const jobList = document.getElementById("jobList");
        jobList.innerHTML = "";

        jobs.forEach(entry => {
            const li = document.createElement("li");
            li.textContent = entry.job;
            jobList.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching jobs:", error);
    }
}

// Initially fetch jobs
fetchJobs();
