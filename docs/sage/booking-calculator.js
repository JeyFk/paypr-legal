(function () {
  'use strict';
  var form = document.querySelector('[data-paypr-booking]');
  if (!form) return;
  var result = document.getElementById('calc-results'), error = document.getElementById('calc-error');
  var money = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'});
  var current;
  function calculate() {
    current = null; result.hidden = true;
    try {
      var f = form.elements;
      current = PayprMath.booking(f.rate.value, f.hours.value, f.minutes.value, f.kids.value, f.perkid.value, f.bookings.value);
      document.getElementById('eff').textContent = money.format(current.effectiveRate);
      document.getElementById('book').textContent = money.format(current.booking);
      document.getElementById('wk').textContent = money.format(current.weekly);
      document.getElementById('booking-detail').textContent = current.hours.toFixed(4).replace(/\.?0+$/, '') + ' hours × ' + money.format(current.effectiveRate) + ' per hour. Weekly estimate: ' + current.bookings + (current.bookings === 1 ? ' booking. Straight-time' : ' identical bookings. Straight-time') + ' pay only; check overtime separately.';
      error.textContent = ''; result.hidden = false; return true;
    } catch (e) { error.textContent = e.message; return false; }
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (calculate() && typeof window.payprGoal === 'function') window.payprGoal('calculator_completed', {tool: 'babysitter'});
  });
  form.addEventListener('input', function () { current = null; result.hidden = true; error.textContent = ''; });
  document.getElementById('download-result').addEventListener('click', function () {
    if (!current) return;
    PayprExport.csv('babysitter-pay-summary.csv', [
      ['Item', 'Value', 'Unit'], ['Base hourly rate', form.elements.rate.value, 'USD/hour'],
      ['Children', form.elements.kids.value, 'children'], ['Extra per additional child', form.elements.perkid.value, 'USD/hour'],
      ['Duration', current.hours.toFixed(6), 'hours'], ['Effective hourly rate', current.effectiveRate.toFixed(2), 'USD/hour'],
      ['Booking total', current.booking.toFixed(2), 'USD'], ['Identical bookings per week', current.bookings, 'bookings'],
      ['Weekly straight-time estimate', current.weekly.toFixed(2), 'USD'],
      ['Scope', 'No overtime, tax, reimbursement or other adjustments included', '']
    ]);
  });
  document.getElementById('print-result').addEventListener('click', function () { if (current) window.print(); });
  document.getElementById('calc-button').disabled = false;
  calculate();
}());
