function success_notification(message) {
    setTimeout($.bootstrapGrowl(message, {
            type: "success",
            ele: "body",
            align: "left",
            width: 300,
            allow_dismiss: false,
            stackup_spacing: 3
        }
    ), 2000);
}

function error_notification(data) {
    let error_message = data?.["error"] ? data["error"] : "Something went wrong!";

    setTimeout($.bootstrapGrowl(error_message, {
            type: "danger", // info, success, warning and danger
            ele: "body", // parent container
            align: "left", // right, left or center
            width: 300,
            allow_dismiss: false,
            stackup_spacing: 3
        }
    ), 2000);
}


function actionVisibility(obj, action) {
    let cardBody = $(obj).closest(".card"),
        allTextAreas = cardBody.find('textarea'),
        allInputs = cardBody.find('input'),
        allSelects = cardBody.find('select'),
        allButtons = cardBody.find('button');

    for (let i = 0; i < allButtons.length; i++) {
        if (allButtons[i].style.display === "none") {
            allButtons[i].style.display = "inline";
        } else if (allButtons[i].style.display === "inline") {
            allButtons[i].style.display = "none";
        }
    }
    if (action === "edit") {
        for (let i = 0; i < allSelects.length; i++) {
            allSelects[i].removeAttribute('disabled');
        }
        for (let i = 0; i < allTextAreas.length; i++) {
            allTextAreas[i].removeAttribute('disabled');
        }
        for (let i = 0; i < allInputs.length; i++) {
            allInputs[i].removeAttribute('disabled');
        }
    } else if (action === 'cancel') {
        for (let i = 0; i < allSelects.length; i++) {
            allSelects[i].setAttribute('disabled', true);
        }
        for (let i = 0; i < allTextAreas.length; i++) {
            allTextAreas[i].setAttribute('disabled', true);
        }
        for (let i = 0; i < allInputs.length; i++) {
            allInputs[i].setAttribute('disabled', true);
        }
    }
}


function createQuestion() {
    let mainCard = $('#mainCard');

    $.ajax({
        type: "GET",
        url: `/question/create/`,
        success: function (html_data) {
            mainCard.html(html_data);
        },
        error: function (response) {
            error_notification(response.responseJSON);
        }
    });
}


function getAdminPanel() {

    $.ajax({
        type: "GET",
        url: `/`,
        success: function (html_data) {
            $('body').html(html_data);
        },
        error: function (response) {
            error_notification(response.responseJSON);
        }
    });
}


function createTheme() {
    let mainCard = $('#mainCard');

    $.ajax({
        type: "GET",
        url: `/theme/create/`,
        success: function (html_data) {
            mainCard.html(html_data);
        },
        error: function (response) {
            error_notification(response.responseJSON);
        }
    });
}

$(document).ready(function () {

    let questionsTable = $('#questionsTable').DataTable(),
        themesTable = $('#themesTable').DataTable(),
        mainCard = $('#mainCard');

    questionsTable.on('click', 'tbody tr', function () {
        let question_id = $(this).attr('question-id');
        $.ajax({
            type: "GET",
            url: `/question/${question_id}/`,
            success: function (html_data) {
                mainCard.html(html_data);
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });

    themesTable.on('click', 'tbody tr', function () {
        let theme_id = $(this).attr('theme-id');
        $.ajax({
            type: "GET",
            url: `/theme/${theme_id}/`,
            success: function (html_data) {
                mainCard.html(html_data);
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });

    $("#pushToDatabaseButton").on('click', function (e) {
        $.ajax({
            type: "GET",
            url: "/import/",
            success: function () {
                success_notification("Data successfully added to the database");
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });

    $("#exportFromDatabaseButton").on('click', function (e) {
        $.ajax({
            type: "GET",
            url: "/export/",
            success: function () {
                success_notification("Data successfully exported from the database");
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });
});