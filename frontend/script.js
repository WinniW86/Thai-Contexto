async function submitGuess() {
  const word = document.getElementById("guessInput").value;
  const response = await fetch("/guess", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({word})
  });
  const result = await response.json();

  const list = document.getElementById("results");
  const item = document.createElement("li");
  item.textContent = `${result.guess} → similarity: ${result.similarity.toFixed(3)} ${result.correct ? "✅ ถูกต้อง!" : ""}`;
  list.appendChild(item);
}
