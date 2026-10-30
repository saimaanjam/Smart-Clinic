async function loginPatient(event) {
    event.preventDefault(); // stop page refresh

    console.log("LOGIN FUNCTION TRIGGERED"); // test message

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5000/auth/patient", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        sessionStorage.setItem("patient", JSON.stringify(data.user));
        
        alert("You have successfully logged in!");
        window.location.href = "index.html";
        

    } else {
        alert("Invalid email or password");
    }
}
