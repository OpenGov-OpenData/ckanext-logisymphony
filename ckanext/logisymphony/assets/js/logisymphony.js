ckan.module('logi-dashboards', function (jQuery) {

    return {
        /* Sets up the module, binding methods, creating elements etc. Called
         * internally by ckan.module.initialize();
         *
         * Returns nothing.
         */
        initialize: function () {
            const that = this;

            // Populate dropdown
            $.getJSON(this.options.source, function (data) {
                that.dashboard_list = data.results;
                that.setup();
            });
        },

        formatResult: function (result) {
            var date = (new Date(result.lastModifiedTime));
            var markup = "<div class='dashboard-result'><span class='title'>" + result.name + "</span><span class='modified'>modified " + date.toLocaleDateString() + "</span></div>";
            return markup;
        },

        // Display thumbnail when dashboard is selected
        onSelectDashboard: function(id) {
            var dashboard = $.grep(this.dashboard_list, function(e){ return e.id == id; })[0];
            $('#field-title').val(dashboard.name).trigger('keyup');
            $('.dashboard-thumbnail .media-image').attr('src', 'https://logi-sandbox.ogopendata.com/managed/Resource/GetStoredViewThumbnail/?viewId='+dashboard.id);
        },

        setup: function () {
            const that = this;
            var settings = {
                width: 'resolve',
                id: 'id',
                dropdownCssClass: 'selectorContainer',
                containerCssClass: 'selectorContainer',
                formatResult: this.formatResult,
                formatSelection: function (result) {
                    return result.name;
                },
                formatNoMatches: this.formatNoMatches,
                formatInputTooShort: this.formatInputTooShort,
                escapeMarkup: function (markup) {
                    return markup;
                },
                matcher: function(term, text) {
                    return text.toUpperCase().indexOf(term.toUpperCase()) >= 0;
                },
                data: this.dashboard_list
            };

            var select2 = this.el.select2(settings);

            this.el.on("change", function(e) {
                const id = e.target.value;
                that.onSelectDashboard(id);
            });

            this._select2 = select2;
        },
    };
});
