/* Paypr planning tools. US federal examples; not a payroll engine. */
(function (root) {
  'use strict';
  function number(value, label, maximum) {
    if (value === null || value === undefined || String(value).trim() === '') throw new Error('Enter ' + label + '.');
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
  function integer(value, label, maximum) {
    var n = number(value, label, maximum);
    if (!Number.isInteger(n)) throw new Error('Enter a whole number for ' + label + '.');
    return n;
  }
  function booking(rate, hours, minutes, children, extra, bookings) {
    rate = number(rate, 'hourly rate', 10000);
    hours = integer(hours, 'hours', 24);
    minutes = integer(minutes, 'minutes', 59);
    children = integer(children, 'children', 20);
    extra = number(extra, 'extra pay per additional child', 10000);
    bookings = integer(bookings, 'bookings per week', 31);
    if (children < 1 || bookings < 1) throw new Error('Enter at least one child and one booking.');
    var duration = hours + minutes / 60;
    if (duration <= 0 || duration > 24) throw new Error('Enter a booking longer than zero and no longer than 24 hours.');
    if (duration * bookings > 168) throw new Error('The bookings cannot total more than 168 hours in a week.');
    var effectiveRate = rate + extra * (children - 1);
    return {hours: duration, effectiveRate: effectiveRate, booking: effectiveRate * duration,
      weekly: effectiveRate * duration * bookings, bookings: bookings};
  }
  function shift(start, end, breakMinutes, overnight) {
    if (!start && !end) {
      if (Number(breakMinutes) !== 0 || overnight) throw new Error('Enter shift times or clear its break and next-day setting.');
      return 0;
    }
    function clock(value) {
      if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(value)) throw new Error('Enter both start and end times.');
      var parts = value.split(':').map(Number);
      return parts[0] * 60 + parts[1];
    }
    var elapsed = clock(end) - clock(start) + (overnight ? 1440 : 0);
    if (elapsed <= 0 || elapsed > 1440) throw new Error('Check shift times and “Ends next day”; each row must span more than zero and at most 24 hours.');
    var unpaid = integer(breakMinutes, 'unpaid break minutes', 1440);
    if (unpaid >= elapsed) throw new Error('The unpaid break must be shorter than the shift.');
    return elapsed - unpaid;
  }
  var api = {wages: wages, fica2026: fica2026, booking: booking, shift: shift};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.PayprMath = api;
}(typeof window === 'undefined' ? this : window));
