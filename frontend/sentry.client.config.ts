import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  tracesSampleRate: 1.0,
  beforeSend(event) {
    if (event.level === 'fatal') {
      // Send an immediate alert
      sendAlertToTeam(event);
    }
    return event;
  },
});

function sendAlertToTeam(event: Sentry.Event) {
  // Implement your alert mechanism here (e.g., send an email, Slack message, etc.)
}
