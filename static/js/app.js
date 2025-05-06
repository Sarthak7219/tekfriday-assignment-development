// Tab switching
const tabs = document.querySelectorAll(".tab");
tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    document
      .querySelectorAll(".section")
      .forEach((s) => s.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.target).classList.add("active");
  });
});

// Chatbot
document.getElementById("sendChat").addEventListener("click", async () => {
  const question = document.getElementById("question").value;
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  const { answer } = await res.json();
  document.getElementById("chatResponse").textContent = answer;
});

// Single Risk Calculator
document.getElementById("calcRisk").addEventListener("click", async () => {
  const payload = {
    missed_repayments: Number(document.getElementById("missed").value),
    loan_amount: Number(document.getElementById("loan").value),
    collateral_value: Number(document.getElementById("collateral").value),
    interest: Number(document.getElementById("interest").value),
  };
  const res = await fetch("/calculate-risk", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  document.getElementById(
    "riskResponse"
  ).textContent = `Score: ${data.score}, Level: ${data.risk_level}`;
});

// Batch Risk Tagging - Trigger backend and show message
document.getElementById("uploadDataset").addEventListener("click", async () => {
  const output = document.getElementById("batchResponse");
  output.textContent = "Processing...may take time";
  try {
    await fetch("/batch-risk");
    output.textContent = "✅ Risk tagging completed for dataset.";
  } catch (error) {
    console.error("Batch tagging failed:", error);
    output.textContent = "❌ Failed to tag dataset.";
  }
});
