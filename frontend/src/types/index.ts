export interface GuideRequest {
  question: string;
  api_key: string;
  model: string;
}

export interface GuideSuccessResponse {
  status: "success";
  role: string;
  response: string;
  pdf_path: string;
}

export interface GuideErrorResponse {
  status: "failed";
  message: string;
}

export type GuideResponse = GuideSuccessResponse | GuideErrorResponse;

export interface GeneratedGuide {
  role: string;
  content: string;
  pdfUrl: string;
}

export interface TocHeading {
  id: string;
  text: string;
  level: number;
}

export const LOADING_STEPS = [
  "Understanding Request",
  "Identifying Role",
  "Searching Knowledge Base",
  "Building Roadmap",
  "Finding Resources",
  "Generating Projects",
  "Preparing Interview Questions",
  "Writing Resume Tips",
  "Creating PDF",
] as const;

export const PROMPT_CHIPS = [
  "Generate AI Engineer Guide",
  "Generate Data Engineer Guide",
  "Generate DevOps Guide",
  "Generate Software Engineer Guide",
  "Generate Full Stack Guide",
] as const;

export const BACKEND_URL = "http://localhost:8000";