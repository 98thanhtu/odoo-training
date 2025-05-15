odoo.define('project_management.ClickableInteger', function (require) {
  "use strict";

  var fieldRegistry = require('web.field_registry');
  var ListFieldInteger = require('web.ListFieldInteger');

  var ClickableInteger = ListFieldInteger.extend({
    events: _.extend({}, ListFieldInteger.prototype.events, {
      'click': '_onClick',
    }),
    _render: function () {
      this._super.apply(this, arguments);
      this.$el.addClass('o_clickable_field');
      this.$el.css('cursor', 'pointer');
    },
    _onClick: function (ev) {
      ev.stopPropagation();
      var clickAction = this.nodeOptions.click_action;
      if (clickAction) {
        var recordId = this.recordData.id;
        this._rpc({
          model: this.model,
          method: clickAction,
          args: [recordId],
          context: this.recordData,
        }).then(function (action) {
          if (action) {
            return this.do_action(action);
          }
        });
      }
    },
  });

  fieldRegistry.add('clickable_integer', ClickableInteger);

  return ClickableInteger;
});
