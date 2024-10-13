import express from 'express';
import logger from './utils/logger';
import { handle_exception } from './middleware/error_handler';

const app = express();

// ... other middleware and route setup

app.use(handle_exception);

app.listen(3000, () => {
  logger.info('Server started on port 3000');
});
