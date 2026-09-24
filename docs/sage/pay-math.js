/* Paypr planning tools. US federal examples; not a payroll engine. */
(function (root) {
  'use strict';
  function number(value, label, maximum) {
    if (value === '' || value === null || value === undefined) throw new Error('Enter ' + label + '.');
    var n = Number(value);
    if (!Number.isFinite(n) || n < 0 || (maximum !== undefined && n > maximum)) {
      throw new Error('Enter ' + label + (maximum !== undefined ? ' between 0 and ' + maximum : ' of zero or more') + '.');
    }
    return n;
  }
  function wages(rate, hours, weeks) {
    rate = number(rate, 'hourly rate', 10000);
    hours = number(hours, 'weekly hours', 168);
    weeks = number(weeks, 'paid weeks', 52);
    var regularHours = Math.min(hours, 40), overtimeHours = Math.max(hours - 40, 0);
    var regularPay = regularHours * rate, overtimePay = overtimeHours * rate * 1.5;
    var weekly = regularPay + overtimePay, annual = weekly * weeks;
    return {regularHours: regularHours, overtimeHours: overtimeHours, regularPay: regularPay,
      overtimePay: overtimePay, weekly: weekly, annual: annual, monthly: annual / 12};
  }
  function fica2026(annualWages) {
    var annual = number(annualWages, 'annual cash wages', 10000000);
    var socialSecurity = annual >= 3000 ? Math.min(annual, 184500) * 0.062 : 0;
    var medicare = annual >= 3000 ? annual * 0.0145 : 0;
    return {socialSecurity: socialSecurity, medicare: medicare, employerFica: socialSecurity + medicare};
  }
  var api = {wages: wages, fica2026: fica2026};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.PayprMath = api;
}(typeof window === 'undefined' ? this : window));
