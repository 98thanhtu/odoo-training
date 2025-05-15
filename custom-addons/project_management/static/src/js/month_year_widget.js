odoo.define('project_management.MonthYearWidget', [
  'web.field_registry',
  'web.AbstractField',
  'web.DatePicker',
  'moment'
], function (require) {
  "use strict";

  var fieldRegistry = require('web.field_registry');
  var AbstractField = require('web.AbstractField');
  var DatePicker = require('web.DatePicker');
  var moment = require('moment');

  var MonthYearWidget = AbstractField.extend({
    template: 'MonthYearWidget',
    start: function () {
      this._super.apply(this, arguments);
      this._initDatePicker();
    },
    _initDatePicker: function () {
      var self = this;
      this.$input = this.$el.find('input');
      this.$input.datepicker({
        format: 'mm/yyyy',
        viewMode: 'months',
        minViewMode: 'months',
        autoclose: true,
      }).on('changeDate', function (e) {
        var date = moment({ year: e.date.getFullYear(), month: e.date.getMonth(), date: 1 });
        self._setValue(date.format('YYYY-MM-DD'));
      });
      if (this.value) {
        var date = moment(this.value);
        this.$input.datepicker('update', date.format('MM/YYYY'));
      }
    },
    _setValue: function (value) {
      this._super.apply(this, [value]);
      this.$input.datepicker('update', moment(value).format('MM/YYYY'));
    },
  });

  fieldRegistry.add('month_year', MonthYearWidget);

  return MonthYearWidget;
});
