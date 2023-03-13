$(document).ready(function () {
    $("#addThemeForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray()
        $.ajax({
            type: "POST",
            url: "/theme/create/",
            data: submitForm,
            success: function () {
                getAdminPanel();
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });

    });
});