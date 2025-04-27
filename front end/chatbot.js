function sendMessage() {
  const userInputField = document.getElementById('userInput');
  const chatbox = document.getElementById('chatbox');
  const userText = userInputField.value.trim();

  if (userText === '') return;

  // Display user message
  const userMessage = document.createElement('p');
  userMessage.textContent = "🧍 You: " + userText;
  chatbox.appendChild(userMessage);

  // Bot response logic
  const botMessage = document.createElement('p');
  botMessage.style.color = 'lightgreen';
  let botResponse = "🤖 DermoBot: ";

  const lowerText = userText.toLowerCase();

  if (lowerText.includes("melanoma")) {
    botResponse += "Melanoma is a dangerous type of skin cancer that can spread quickly. Early detection is vital. Please consult a dermatologist.";
  } else if (lowerText.includes("melanocytic nevi")) {
    botResponse += "Melanocytic Nevi, also known as moles, are usually benign but should be monitored for changes in shape, color, or size.";
  } else if (lowerText.includes("benign keratosis")) {
    botResponse += "Benign keratosis includes non-cancerous growths like seborrheic keratosis. These are harmless but can be removed if bothersome.";
  } else if (lowerText.includes("basal cell carcinoma")) {
    botResponse += "Basal Cell Carcinoma is a common skin cancer. It's usually treatable and rarely spreads, but requires medical evaluation.";
  } else if (lowerText.includes("actinic keratosis") || lowerText.includes("iec")) {
    botResponse += "Actinic Keratosis (IEC) are rough, scaly patches caused by sun damage. They can develop into skin cancer if untreated.";
  } else if (lowerText.includes("vascular lesion")) {
    botResponse += "Vascular Lesions are abnormal blood vessels that can appear as red or purple spots. Many are harmless, but some may need treatment.";
  } else if (lowerText.includes("dermatofibroma")) {
    botResponse += "Dermatofibroma is a small, firm skin nodule. It’s benign and usually doesn’t require treatment unless it causes discomfort.";
  } else if (lowerText.includes("treatment")) {
    botResponse += "Please specify the skin disease you're asking about so I can provide the appropriate treatment options.";
  } else if (lowerText.includes("hello") || lowerText.includes("hi")) {
    botResponse += "Hey there! I'm DermoBot 👨‍⚕️. Ask me about any skin condition and I’ll do my best to help.";
  } else {
    botResponse += "Hmm... I’m not sure how to answer that. Try asking me about a specific skin disease like melanoma or actinic keratosis.";
  }

  botMessage.textContent = botResponse;
  chatbox.appendChild(botMessage);

  userInputField.value = "";
  chatbox.scrollTop = chatbox.scrollHeight;
}
