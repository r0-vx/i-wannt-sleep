# Privacy engineering

ForwardCheck is user-initiated. It must not read private chats automatically, monitor groups, track forwarding behavior, or send rebuttals without approval.

The current local slice stores original text, optional caption, claims, rhetoric spans, retrieved public passages, source metadata, model conclusions, and job events. Access is scoped to a random guest session identifier stored by the browser. Text and evidence are sent to configured Gemini and Brave providers only during a user-started investigation.

Before public deployment, implement enforced expiry, full export, complete deletion across database/object storage/backups, consent records, data-processing disclosures, account controls, redacted structured logging, and organization-approved legal text. Do not submit sensitive personal information to the development build.

