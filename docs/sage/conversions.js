/* Content-free goals only: never send names, form values, wages, or hours. */
(function () {
  'use strict';
  if (location.hostname !== 'usepaypr.com' && location.hostname !== 'www.usepaypr.com') return;
  var allowedPages = new Set(['/', '/nanny-pay-calculator', '/nanny-tax-calculator', '/nanny-timesheet-template', '/how-to-track-what-you-owe-your-nanny']);
  var localizedSlugs = new Set(['', 'support', 'privacy', 'terms', 'about', 'guides', 'how-to-track-what-you-owe-your-nanny', 'nanny-timesheet-template']);
  var markets = {'/es/espana/horas-y-pagos-en-casa': 'ES', '/es/mexico/horas-y-pagos-en-casa': 'MX'};
  function pageContext() {
    var path = location.pathname;
    var localized = path.match(/^\/(es|fr|de|ar)\/(.*)$/);
    if (localized && (localizedSlugs.has(localized[2]) || Object.prototype.hasOwnProperty.call(markets, path))) {
      return {page: path, language: localized[1], content_market: markets[path] || 'global'};
    }
    return {page: allowedPages.has(path) ? path : 'other_resource', language: 'en', content_market: 'global'};
  }
  var allowedGoals = new Set(['app_store_click', 'template_download', 'calculator_completed']);
  window.payprGoal = function (goal, details) {
    if (!allowedGoals.has(goal) || typeof window.datafast !== 'function') return;
    var metadata = pageContext();
    if (details && ['wages', 'fica'].includes(details.tool)) metadata.tool = details.tool;
    if (details && ['header', 'content', 'footer'].includes(details.placement)) metadata.placement = details.placement;
    if (details && ['timesheet', 'example', 'payment_log', 'other'].includes(details.asset)) metadata.asset = details.asset;
    try { window.datafast(goal, metadata); } catch (_) { /* Navigation must still work. */ }
  };
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var url = new URL(link.href, location.href);
    if (url.hostname === 'apps.apple.com') {
      window.payprGoal('app_store_click', {placement: link.closest('header') ? 'header' : link.closest('footer') ? 'footer' : 'content'});
    } else if (url.origin === location.origin && url.pathname.startsWith('/downloads/') && link.hasAttribute('download')) {
      var asset = url.pathname.includes('payment-log') ? 'payment_log' : url.pathname.includes('example') ? 'example' : url.pathname.endsWith('nanny-timesheet.csv') ? 'timesheet' : 'other';
      window.payprGoal('template_download', {asset: asset});
    }
  });
}());
