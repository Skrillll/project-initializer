import { createErrorResponse } from '../utils/errorResponse';

export async function createUser(req: Request, res: Response) {
  try {
    // User creation logic
  } catch (error) {
    const errorResponse = createErrorResponse('USER_CREATION_FAILED', 'Failed to create user', { error: error.message });
    res.status(500).json(errorResponse);
  }
}
