$(document).on('change', '.mark-correct-btn', function() {
    const answerId = $(this).data('answer-id');
    const questionId = $(this).data('question-id');
    const isCorrect = $(this).prop('checked');

    const url = $(this).data('url');
    const csrfToken = $(this).data('csrf');

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            answer_id: answerId,
            question_id: questionId,
            is_correct: isCorrect.toString(),
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            if (response.status !== 'success')
                alert('Произошла ошибка!');
        },
        error: function() {
            alert('Ошибка при отправке запроса!');
        }
    });
});

$(document).on('click', '.like-answer-btn, .dislike-answer-btn', function() {
    const answerId = $(this).data('answer-id');
    const action = $(this).data('action');

    const url = $(this).data('url');
    const csrfToken = $(this).data('csrf');

    $.ajax({
        url: url,
        type: 'POST',
        cache: false,
        data: {
            answer_id: answerId,
            action: action,
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            if (response.new_rating !== undefined) {
                $('#answer-rating-' + answerId).text(response.new_rating);

                // Обновляем классы кнопок
                const likeButton = $('[data-answer-id="' + answerId + '"][data-action="like"]');
                const dislikeButton = $('[data-answer-id="' + answerId + '"][data-action="dislike"]');

                if (response.is_liked) {
                    likeButton.addClass('text-primary').removeClass('text-secondary');
                    dislikeButton.addClass('text-secondary').removeClass('text-primary');
                } else if (response.is_disliked) {
                    dislikeButton.addClass('text-primary').removeClass('text-secondary');
                    likeButton.addClass('text-secondary').removeClass('text-primary');
                } else {
                    // Сбрасываем оба состояния
                    likeButton.addClass('text-secondary').removeClass('text-primary');
                    dislikeButton.addClass('text-secondary').removeClass('text-primary');
                }
            } else {
                alert('Ошибка при обновления счетчитка лайков!');
            }
        },
        error: function(e) {
            alert('Ошибка: ' + e.responseJSON.error);
        }
    });
});
