(function () {
  'use strict';
  var form = document.querySelector('[data-paypr-timesheet]');
  if (!form) return;
  var result = document.getElementById('sheet-results'), error = document.getElementById('sheet-error');
  var money = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'});
  var current = null;
  function calculate() {
    current = null; result.hidden = true;
    try {
      var week = form.elements.week.value;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(week)) throw new Error('Choose the first date of your workweek.');
      var date = new Date(week + 'T12:00:00Z');
      if (isNaN(date) || date.toISOString().slice(0, 10) !== week) throw new Error('Enter a valid workweek date.');
      var rows = [], total = 0;
      for (var i = 0; i < 7; i++) {
        var f = form.elements, start = f['start' + i].value, end = f['end' + i].value;
        var next = f['next' + i].checked, unpaid = f['break' + i].value;
        var minutes;
        try { minutes = PayprMath.shift(start, end, unpaid, next); }
        catch (e) { throw new Error('Day ' + (i + 1) + ': ' + e.message); }
        if (i < 6 && next && minutes && f['start' + (i + 1)].value && f['start' + (i + 1)].value < end) throw new Error('Day ' + (i + 2) + ': this shift overlaps the previous overnight shift.');
        if (i === 6 && next) throw new Error('Split the last overnight shift at the workweek boundary using the blank CSV; it spans two workweeks.');
        total += minutes;
        rows.push([date.toISOString().slice(0, 10), start, end, next ? 'yes' : 'no', unpaid, (minutes / 60).toFixed(6), f.rate.value]);
        date.setUTCDate(date.getUTCDate() + 1);
      }
      if (!total) throw new Error('Enter at least one worked shift.');
      var pay = PayprMath.wages(form.elements.rate.value, total / 60, 1);
      current = {rows: rows, total: total, pay: pay, week: week};
      document.getElementById('sheet-period').textContent = 'Workweek starting ' + week + ' · Hourly rate: ' + money.format(Number(form.elements.rate.value)) + ' USD.';
      document.getElementById('sheet-hours').textContent = Math.floor(total / 60) + 'h ' + total % 60 + 'm';
      document.getElementById('sheet-pay').textContent = money.format(pay.weekly);
      document.getElementById('sheet-detail').textContent = pay.regularHours.toFixed(2) + ' regular hours + ' + pay.overtimeHours.toFixed(2) + ' overtime hours at 1.5×. Gross wages before deductions; one hourly rate.';
      var body = document.getElementById('sheet-preview'); body.replaceChildren();
      rows.filter(function (r) { return r[1]; }).forEach(function (row) {
        var tr = document.createElement('tr');
        [row[0], row[1] + '–' + row[2] + (row[3] === 'yes' ? ' (+1 day)' : ''), row[4], Number(row[5]).toFixed(2)].forEach(function (value) {
          var td = document.createElement('td'); td.textContent = value; tr.appendChild(td);
        }); body.appendChild(tr);
      });
      error.textContent = ''; result.hidden = false; return true;
    } catch (e) { error.textContent = e.message; return false; }
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (calculate() && typeof window.payprGoal === 'function') window.payprGoal('calculator_completed', {tool: 'timesheet'});
  });
  form.addEventListener('input', function () { current = null; result.hidden = true; error.textContent = ''; });
  document.getElementById('sheet-download').addEventListener('click', function () {
    if (!current) return;
    var rows = [['Date', 'Start', 'End', 'Ends next day', 'Unpaid break minutes', 'Paid hours', 'Hourly rate USD']].concat(current.rows);
    rows.push(['TOTAL', '', '', '', '', (current.total / 60).toFixed(6), '']);
    rows.push(['Weekly gross wages USD', current.pay.weekly.toFixed(2), '', '', '', '', '']);
    rows.push(['Regular hours', current.pay.regularHours, '', '', '', '', '']);
    rows.push(['Overtime hours at 1.5x', current.pay.overtimeHours, '', '', '', '', '']);
    rows.push(['Scope: one rate; overtime after 40 hours; excludes taxes, benefits and leave adjustments', '', '', '', '', '', '']);
    PayprExport.csv('nanny-timesheet-' + current.week + '.csv', rows);
  });
  document.getElementById('sheet-print').addEventListener('click', function () {
    if (!current) return;
    document.body.classList.add('print-filled-sheet'); window.print();
  });
  window.addEventListener('afterprint', function () { document.body.classList.remove('print-filled-sheet'); });
  document.getElementById('sheet-button').disabled = false;
}());
