interface ErrorResponse {
  code: string;
  message: string;
  timestamp: string;
  details?: any;
}

export function createErrorResponse(code: string, message: string, details?: any): ErrorResponse {
  return {
    code,
    message,
    timestamp: new Date().toISOString(),
    details,
  };
}
