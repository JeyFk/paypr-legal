// DataFast AI crawler tracking.
//
// Why this file exists: the browser script in each page's <head> only fires for
// visitors that execute JavaScript. AI crawlers (ClaudeBot, GPTBot, ChatGPT-User,
// PerplexityBot, Googlebot...) request raw HTML and never run it, so they are
// invisible to the browser script. This Pages Function sees the request itself
// and reports crawler hits to DataFast's "Bot traffic" card.
//
// Runs on every request NOT excluded by docs/_routes.json — keep robots.txt,
// llms.txt and sitemap.xml routed here, since bots usually fetch those first.
//
// Contract: do NOT await trackAICrawlerRequest. Call it, hand it the context so
// it can use ctx.waitUntil internally, and return the response immediately. The
// DataFast request finishes in the background and must never delay the page.
import { trackAICrawlerRequest } from "@datafast/ai-crawl";

// Same public website ID as the browser script in the page <head>. Not a secret.
const DATAFAST_WEBSITE_ID = "dfid_hJ2Kroo4GcBHH6S3fdlZU";

// Minimal shape of the Cloudflare Pages Function context, typed here so this
// file needs no @cloudflare/workers-types dependency.
type PagesContext = {
  request: Request;
  env: { DATAFAST_BOT_TOKEN?: string };
  next: () => Promise<Response>;
  waitUntil: (promise: Promise<unknown>) => void;
};

export async function onRequest(context: PagesContext) {
  trackAICrawlerRequest(context.request, context, {
    websiteId: DATAFAST_WEBSITE_ID,
    // Optional, and unset today: enforcement is off until "Reject unauthenticated
    // requests" is turned on in the Bot traffic card. To enable, create a dfbot_
    // token there and add it as an encrypted Pages env var — never commit it.
    authToken: context.env.DATAFAST_BOT_TOKEN,
  });

  return context.next();
}
