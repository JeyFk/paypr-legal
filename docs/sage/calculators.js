(function () {
  'use strict';
  var form = document.querySelector('[data-paypr-calculator]');
  if (!form) return;
  var money = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'});
  var kind = form.dataset.payprCalculator;
  var current = null;
  function show(id, value) { document.getElementById(id).textContent = money.format(value); }
  function calculate() {
    var error = document.getElementById('calc-error');
    var result = document.getElementById('calc-results');
    current = null;
    try {
      if (kind === 'wages') {
        var pay = PayprMath.wages(form.elements.rate.value, form.elements.hours.value, form.elements.weeks.value);
        current = pay;
        show('wk', pay.weekly); show('mo', pay.monthly); show('yr', pay.annual);
        document.getElementById('otnote').textContent = pay.regularHours + ' regular hours (' + money.format(pay.regularPay) + ') + ' + pay.overtimeHours + ' overtime hours (' + money.format(pay.overtimePay) + '). Monthly average = annual wages ÷ 12; actual calendar-month pay varies.';
      } else {
        var tax = PayprMath.fica2026(form.elements.annual.value);
        show('ss', tax.socialSecurity); show('medicare', tax.medicare); show('fica', tax.employerFica);
        document.getElementById('taxnote').textContent = Number(form.elements.annual.value) < 3000 ? 'Below the 2026 federal household FICA threshold under the assumptions above. This does not mean that no taxes, reporting, or state obligations apply.' : 'Employer FICA only. FUTA, state taxes, insurance, benefits, and payroll fees are not included.';
      }
      error.textContent = ''; result.hidden = false; return true;
    } catch (e) { result.hidden = true; error.textContent = e.message; return false; }
  }
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (calculate() && typeof window.payprGoal === 'function') window.payprGoal('calculator_completed', {tool: kind});
  });
  form.addEventListener('input', function () {
    current = null;
    document.getElementById('calc-results').hidden = true;
    document.getElementById('calc-error').textContent = '';
  });
  var download = document.getElementById('download-result');
  if (kind === 'wages' && download) {
    download.addEventListener('click', function () {
      if (!current) return;
      PayprExport.csv('nanny-wage-estimate.csv', [
        ['Item', 'Value', 'Unit'], ['Hourly rate', form.elements.rate.value, 'USD/hour'],
        ['Weekly hours actually worked', form.elements.hours.value, 'hours'],
        ['Paid weeks at this schedule', form.elements.weeks.value, 'weeks'],
        ['Regular hours', current.regularHours, 'hours/week'], ['Overtime hours', current.overtimeHours, 'hours/week'],
        ['Regular pay', current.regularPay.toFixed(2), 'USD/week'], ['Overtime pay', current.overtimePay.toFixed(2), 'USD/week'],
        ['Weekly gross wages', current.weekly.toFixed(2), 'USD'], ['Monthly average', current.monthly.toFixed(2), 'USD'],
        ['Annual wages', current.annual.toFixed(2), 'USD'],
        ['Scope', 'One regular rate; 1.5x after 40 hours per week; excludes deductions, employer taxes, benefits and leave adjustments', '']
      ]);
    });
    document.getElementById('print-result').addEventListener('click', function () { if (current) window.print(); });
  }
  document.getElementById('calc-button').disabled = false;
  calculate();
}());
