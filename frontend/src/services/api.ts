import axios from "axios";
import { GuideRequest, GuideResponse, BACKEND_URL } from "@/types";

const apiClient = axios.create({
  baseURL: BACKEND_URL,
  timeout: 120000,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function generateGuide(request: GuideRequest): Promise<GuideResponse> {
  const response = await apiClient.post<GuideResponse>("/guide/generate", request);
  return response.data;
}

export function getPdfDownloadUrl(pdfPath: string): string {
  if (pdfPath.startsWith("http")) return pdfPath;

  const filename = pdfPath.split("/").pop();

  return `${BACKEND_URL}/guide/download/${encodeURIComponent(filename!)}`;
}
