const { withSentryConfig } = require('@sentry/nextjs');

const moduleExports = {
  // Your existing Next.js config
};

const SentryWebpackPluginOptions = {
  // Additional config options for the Sentry webpack plugin. Keep this as is.
};

module.exports = withSentryConfig(moduleExports, SentryWebpackPluginOptions);
