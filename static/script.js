async function sendQuestion() {
  const question = document.getElementById("questionInput").value;
  const classification = document.getElementById("classification");
  const responseText = document.getElementById("responseText");

  if (!question.trim()) {
    alert("Please enter a question.");
    return;
  }

  classification.textContent = "Thinking...";
  responseText.textContent = "";

  try {
    const res = await fetch("/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    classification.textContent = data.classification || "N/A";
    responseText.textContent = data.response || "No response found.";
  } catch (err) {
    classification.textContent = "Error";
    responseText.textContent = "Something went wrong!";
    console.error(err);
  }
}
