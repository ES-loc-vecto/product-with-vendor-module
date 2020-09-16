odoo.define('locations_quants_report.tree_view_button', function (require){
    "use strict";       
    var core = require('web.core');
    var ListView = require('web.ListView'); 
    var ListController = require("web.ListController");


    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.modelName == 'res.partner') {
                var your_btn = this.$buttons.find('button.o_list_button_custom_print');
                your_btn.on('click', this.proxy('o_list_button_custom_print'));
            }
        },
        o_list_button_custom_print: function(e){
            e.preventDefault();
            var context = e.currentTarget.dataset.context;
            this.do_action({
                name: "Google map",
                type: 'ir.actions.act_window',
                res_model: 'res.partner',
                view_mode: 'map',
                view_type: 'map',
                views: [[false, 'map']],
                target: 'new',
                context: context,
                domain: [['name', '=', 'ABCC']],
            });
        }
    };

    ListController.include(includeDict);
});


