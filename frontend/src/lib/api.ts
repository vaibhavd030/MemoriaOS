/**
 * API client for MemoriaOS Backend.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export interface ChatResponsePart {
  type: "text" | "image";
  content: string;
  mime_type?: string;
}

export interface ChatResponse {
  response: ChatResponsePart[];
  status: "success" | "error";
}

/**
 * Sends a chat message with an optional image to the backend.
 */
export async function sendChatMessage(
  message: string,
  imageFile?: File,
  userId: string = "default",
  sessionId: string = "default_session"
): Promise<ChatResponse> {
  const formData = new FormData();
  formData.append("message", message);
  formData.append("user_id", userId);
  formData.append("session_id", sessionId);
  
  if (imageFile) {
    formData.append("image", imageFile);
  }

  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(errorData.detail || "Failed to send message");
  }

  return response.json();
}

/**
 * Fetches generated reels from the backend.
 */
export async function getReels() {
  const response = await fetch(`${API_BASE_URL}/api/reels`);
  if (!response.ok) throw new Error("Failed to fetch reels");
  return response.json();
}

/**
 * Initiates the Google Photos connection flow.
 */
export async function connectPhotos() {
  const response = await fetch(`${API_BASE_URL}/api/photos/connect`);
  if (!response.ok) throw new Error("Failed to connect photos");
  return response.json();
}

/**
 * Establishes a WebSocket connection for Gemini Live.
 */
export function createLiveSession() {
  const wsUrl = API_BASE_URL.replace(/^http/, "ws") + "/api/live";
  return new WebSocket(wsUrl);
}
