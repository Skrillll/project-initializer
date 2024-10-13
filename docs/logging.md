# Logging

This document outlines the logging mechanisms used in our application.

We use Winston for logging in our backend. Logs are stored in the `logs` directory and rotated daily.

Usage:

```typescript
import logger from '../utils/logger';
logger.info('This is an info message', { context: 'additional info' });
logger.error('This is an error message', { error: new Error('Something went wrong') });
```
