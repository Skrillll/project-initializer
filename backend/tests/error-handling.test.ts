import request from 'supertest';
import app from '../src/app';
import { ValidationError } from '../src/utils/customErrors';

describe('Error Handling', () => {
  it('should return 400 for ValidationError', async () => {
    app.get('/test-validation-error', () => {
      throw new ValidationError('Test validation error');
    });

    const response = await request(app).get('/test-validation-error');
    expect(response.status).toBe(400);
    expect(response.body).toHaveProperty('code', 'VALIDATION_ERROR');
  });

  it('should return 500 for unexpected errors', async () => {
    app.get('/test-unexpected-error', () => {
      throw new Error('Unexpected error');
    });

    const response = await request(app).get('/test-unexpected-error');
    expect(response.status).toBe(500);
    expect(response.body).toHaveProperty('code', 'INTERNAL_SERVER_ERROR');
  });
});
