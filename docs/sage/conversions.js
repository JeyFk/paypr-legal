/* Content-free goals only: never send names, form values, wages, or hours. */
(function () {
  'use strict';
  if (location.hostname !== 'usepaypr.com' && location.hostname !== 'www.usepaypr.com') return;
  var allowedPages = new Set(['/', '/nanny-pay-calculator', '/nanny-tax-calculator', '/nanny-timesheet-template', '/how-to-track-what-you-owe-your-nanny']);
  function pageName() { return allowedPages.has(location.pathname) ? location.pathname : 'other_resource'; }
  var allowedGoals = new Set(['app_store_click', 'template_download', 'calculator_completed']);
  window.payprGoal = function (goal, details) {
    if (!allowedGoals.has(goal) || typeof window.datafast !== 'function') return;
    var metadata = {page: pageName()};
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
