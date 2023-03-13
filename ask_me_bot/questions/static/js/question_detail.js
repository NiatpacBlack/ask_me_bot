$(document).ready(function () {
    $("#editQuestionForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray(),
            question_id = $(this).attr('question-id'),
            incorrect_answers_id = $(this).attr('incorrect-answers-id'),
            correct_answer_id = $(this).attr('correct-answer-id');

        submitForm.push({"name": "incorrect_answers_id", "value": incorrect_answers_id})
        submitForm.push({"name": "correct_answers_id", "value": correct_answer_id})

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