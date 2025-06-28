async function sendQuestion() {
  const question = document.getElementById("questionInput").value;
  const classification = document.getElementById("classification");
  const responseText = document.getElementById("responseText");
  const originalText = document.getElementById("originalText");
  const translatedText = document.getElementById("translatedText");


  if (!question.trim()) {
    alert("Please enter a question.");
    return;
  }

  // Set loading UI
  classification.textContent = "Thinking...";
  responseText.innerHTML = "";
  originalText.textContent = "";
  translatedText.textContent = "";

  try {
    const res = await fetch("/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    originalText.textContent = data.original_input || "Unknown";
    translatedText.textContent = data.translated_input || "Already English";
    classification.textContent = data.result?.tag || "Unclassified";


  // Render Markdown in the response
    if (data.result?.response) {
      responseText.innerHTML = DOMPurify.sanitize(marked.parse(data.result.response)); // Markdown → HTML
    } else {
      responseText.textContent = "No response found.";
    }

    // ✅ Play audio if available
   // Show speaking animation
const audioContainer = document.getElementById("audioContainer");
audioContainer.innerHTML = `
  <div class="voice-bars">
    <div class="voice-bar"></div>
    <div class="voice-bar"></div>
    <div class="voice-bar"></div>
  </div>
`;

if (data.result?.audio_url) {
  const audio = new Audio(data.result.audio_url);

  audio.play().catch(err => console.warn("Audio play failed:", err));

  // Remove animation when audio ends
  audio.onended = () => {
    audioContainer.innerHTML = "<p>✅ Done speaking.</p>";
  };
}

  } catch (err) {
    classification.textContent = "Error";
    responseText.textContent = "Something went wrong!";
    console.error(err);
  }
}


function showProcessFlow(stages) {
  const container = document.getElementById("processFlow");
  container.innerHTML = ""; // Clear previous flow

  stages.forEach((stage, index) => {
    const box = document.createElement("div");
    box.className = "process-box";
    box.textContent = stage;

    // Add with animation delay
    setTimeout(() => {
      container.appendChild(box);
    }, index * 200); // Delay each by 200ms
  });
}

showProcessFlow(["", "", ""]);

// showProcessFlow([
//   "User Input",
//   "Language Detection",
//   "Translation",
//   "Classification",
//   "Vector Search",
//   "LLM Response",
//   "Text-to-Speech",
//   "Display",
  
// ]);


