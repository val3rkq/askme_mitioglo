$(document).on('click', '.like-question-btn, .dislike-question-btn', function() {
    const questionId = $(this).data('question-id');
    const action = $(this).data('action');

    const url = $(this).data('url');
    const csrfToken = $(this).data('csrf');

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            question_id: questionId,
            action: action,
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            if (response.new_rating !== undefined) {
                $('#question-rating-' + questionId).text(response.new_rating);
            
                // Обновляем классы кнопок
                const likeButton = $('[data-question-id="' + questionId + '"][data-action="like"]');
                const dislikeButton = $('[data-question-id="' + questionId + '"][data-action="dislike"]');

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
                alert('Error updating rating');
            }
        },
        error: function(e) {
            alert('An error occurred: ' + e.responseJSON.error);
        }
    });
});