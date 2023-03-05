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


function actionQuestion(obj, action) {
    let cardBody = $(obj).closest(".card"),
        allTextAreas = cardBody.find('textarea'),
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
    } else if (action === 'cancel') {
        for (let i = 0; i < allSelects.length; i++) {
            allSelects[i].setAttribute('disabled', true);
        }
        for (let i = 0; i < allTextAreas.length; i++) {
            allTextAreas[i].setAttribute('disabled', true);
        }
    }
}

$(document).ready(function () {

    let questionTable = $('#questionsTable').DataTable();

    questionTable.on('click', 'tbody tr', function () {
        let question_id = $(this).attr('question-id');
        $.ajax({
            type: "GET",
            url: `/question/${question_id}/`,
            success: function () {
                window.location.href = `/question/${question_id}/`;
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });

    });

    $("#addQuestionForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray()
        $.ajax({
            type: "POST",
            url: "/",
            data: submitForm,
            success: function () {
                window.location.href = "/";
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });

    $("#editQuestionForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray(),
            question_id = $(this).attr('question-id'),
            incorrect_answers_id = $(this).attr('incorrect-answers-id'),
            correct_answer_id = $(this).attr('correct-answer-id');

        submitForm.push({"name": "incorrect_answers_id", "value": incorrect_answers_id})
        submitForm.push({"name": "correct_answers_id", "value": correct_answer_id})
        console.log(submitForm)
        $.ajax({
            type: "PUT",
            url: `/question/${question_id}/`,
            data: submitForm,
            success: function () {
                success_notification("Data successfully changed in the database");
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });


    $("#pushToDatabaseButton").on('click', function (e) {
        $.ajax({
            type: "GET",
            url: "/push/",
            success: function () {
                success_notification("Data successfully added to the database");
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });

    $("#editQuestionButton").click(function () {
        actionQuestion(this, 'edit');
    });


    $("#cancelQuestionButton").click(function () {
        actionQuestion(this, 'cancel');
    });

    $("#deleteQuestionButton").click(function () {
        let question_id = $(this).attr('question-id');

        $.confirm({
            title: 'Удалить вопрос',
            content: 'Вы уверены, что хотите удалить этот вопрос?',
            buttons: {
                confirm: function () {
                    $.ajax({
                        type: "DELETE",
                        url: `/question/${question_id}/`,
                        success: function () {
                            window.location.href = "/questions/";
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