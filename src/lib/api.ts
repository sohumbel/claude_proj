/**
 * API service for Resume Roaster backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface JobStatus {
  job_id: string;
  status: "pending" | "analyzing" | "roasting" | "generating" | "completed" | "failed";
  progress: number;
  message: string;
  video_url?: string;
  roast_text?: string;
  score?: number;
  error?: string;
}

export interface UploadResponse {
  job_id: string;
  message: string;
}

export interface RoastResult {
  job_id: string;
  roast_text: string;
  score: number;
  video_url: string;
  issues: Array<{
    category: string;
    severity: string;
    description: string;
  }>;
}

/**
 * Upload a resume file and start processing
 */
export async function uploadResume(file: File, backgroundVideo: string = "subway_surfer"): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("background_video", backgroundVideo);

  const response = await fetch(`${API_BASE_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(error.detail || "Failed to upload resume");
  }

  return response.json();
}

/**
 * Get the status of a processing job
 */
export async function getJobStatus(jobId: string): Promise<JobStatus> {
  const response = await fetch(`${API_BASE_URL}/api/status/${jobId}`);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Status check failed" }));
    throw new Error(error.detail || "Failed to get job status");
  }

  return response.json();
}

/**
 * Get the final result of a completed job
 */
export async function getResult(jobId: string): Promise<RoastResult> {
  const response = await fetch(`${API_BASE_URL}/api/result/${jobId}`);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Failed to get result" }));
    throw new Error(error.detail || "Failed to get result");
  }

  return response.json();
}

/**
 * Get video URL for a job
 */
export function getVideoUrl(jobId: string): string {
  return `${API_BASE_URL}/api/video/${jobId}`;
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<{
  status: string;
  message: string;
  video_generation: string;
  available_backgrounds?: string[];
}> {
  const response = await fetch(`${API_BASE_URL}/`);

  if (!response.ok) {
    throw new Error("API is not available");
  }

  return response.json();
}

/**
 * Get available background videos
 */
export async function getAvailableBackgrounds(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/backgrounds`);

  if (!response.ok) {
    throw new Error("Failed to get backgrounds");
  }

  const data = await response.json();
  return data.backgrounds || [];
}

/**
 * Poll for job completion
 * Returns a promise that resolves when the job is completed or fails
 */
export async function pollJobStatus(
  jobId: string,
  onProgress?: (status: JobStatus) => void,
  intervalMs: number = 2000
): Promise<JobStatus> {
  return new Promise((resolve, reject) => {
    const checkStatus = async () => {
      try {
        const status = await getJobStatus(jobId);

        // Call progress callback if provided
        if (onProgress) {
          onProgress(status);
        }

        // Check if job is complete
        if (status.status === "completed") {
          resolve(status);
          return;
        }

        if (status.status === "failed") {
          reject(new Error(status.error || "Job failed"));
          return;
        }

        // Continue polling
        setTimeout(checkStatus, intervalMs);
      } catch (error) {
        reject(error);
      }
    };

    checkStatus();
  });
}
