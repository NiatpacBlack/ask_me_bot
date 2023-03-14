$(document).ready(function () {
    $("#editThemeForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray(),
            theme_id = $(this).attr('theme-id');

        $.ajax({
            type: "PUT",
            url: `/theme/${theme_id}/`,
            data: submitForm,
            success: function () {
                success_notification("Data successfully changed in the database");
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });


    $("#editThemeButton").click(function () {
        actionVisibility(this, 'edit');
    });


    $("#cancelThemeButton").click(function () {
        actionVisibility(this, 'cancel');
    });

    $("#deleteThemeButton").click(function () {
        let theme_id = $(this).attr('theme-id');

        $.confirm({
            title: 'Удалить тему',
            content: 'Если вы удалите тему, вместе с ней удалятся и вопросы к этой теме. Вы уверены, что хотите удалить эту тему?',
            buttons: {
                confirm: function () {
                    $.ajax({
                        type: "DELETE",
                        url: `/theme/${theme_id}/`,
                        success: function () {
                            getAdminPanel();
                        },
                        error: function (response) {
                            error_notification(response.responseJSON);
                        }
                    });
                },
                cancel: function () {
                    $.alert('Отменено!');
                }
            }
        });
    });
});