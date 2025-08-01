import type { ChatMessage } from "./types";

export async function sendEnhancementRequest(
  file: File,
  history: ChatMessage[]
): Promise<{ newMessage: string; enhancedBlob: Blob }> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("history", JSON.stringify(history));

  const res = await fetch("http://localhost:8000/enhance-resume/", {
    method: "POST",
    body: formData,
  });

  const json = await res.json();
  const base64Pdf = json.enhanced_resume_pdf_b64;
  const message = json.message || "Here is your enhanced resume.";

  // Convert base64 to Blob
  const binary = atob(base64Pdf);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  const blob = new Blob([bytes], { type: "application/pdf" });

  return {
    newMessage: message,
    enhancedBlob: blob,
  };
}
