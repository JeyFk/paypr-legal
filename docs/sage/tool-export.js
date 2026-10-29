/* The generated file stays in the browser; form values are never analytics metadata. */
(function () {
  'use strict';
  window.PayprExport = {
    csv: function (filename, rows) {
      var text = rows.map(function (row) {
        return row.map(function (cell) { return '"' + String(cell).replace(/"/g, '""') + '"'; }).join(',');
      }).join('\r\n') + '\r\n';
      var url = URL.createObjectURL(new Blob(['\ufeff', text], {type: 'text/csv;charset=utf-8'}));
      var link = document.createElement('a');
      link.href = url; link.download = filename;
      document.body.appendChild(link); link.click(); link.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }
  };
}());
