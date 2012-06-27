var Redactor = (function ($) {
    // Redactor palette attributes will accumulate here.
    var redactor_attrs = [];
    // Initialize all textareas with the ``redactor_content`` class
    // as a Redactor rich text area.
    $(document).ready(function () {
        var redactor_fields = $("textarea.redactor_content");
        if (redactor_fields.length !== redactor_attrs.length) {
            window.alert("Number of registered attributes does not match the widget count.");
        }
        $("textarea.redactor_content").each(function (i) {
            var settings = redactor_attrs[i];
            if (settings.in_admin) {
                // Add a class to the field's label in the Django admin so it can
                // be styled as well.
                $(this).parent("div").find("label").addClass("redactor_label");
            }
            // Not a real redactor setting, so this can be removed.
            delete settings.in_admin;
            $(this).redactor(settings);
        });
    });

    return {
        register: function () {
            var attrs = arguments.length !== 0 ? arguments[0] : null;
            redactor_attrs.push(attrs);
        }
    };
})(jQuery);
