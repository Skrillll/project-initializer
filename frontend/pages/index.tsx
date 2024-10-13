import { useEffect } from 'react';
import * as Sentry from "@sentry/nextjs";

const HomePage = () => {
  useEffect(() => {
    try {
      // Some code that might throw an error
    } catch (error) {
      Sentry.captureException(error);
    }
  }, []);

  // ...
};

export default HomePage;
