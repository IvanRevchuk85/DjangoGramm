// ✅ Функция для получения CSRF-токена
function getCSRFToken() {
    return document.getElementById("csrf-token")?.value || null;
}

var csrfToken = getCSRFToken();

console.log("✅ CSRF-токен:", csrfToken);
if (!csrfToken) {
    console.error("❌ Ошибка: CSRF-токен не найден! Проверь HTML-код.");
}

// ✅ Функция лайков
window.toggleLike = function (postId) {
    if (!postId) {
        console.error("❌ Ошибка: postId не определён!");
        return;
    }

    console.log(`🟢 Отправка запроса на лайк для поста ID: ${postId}`);

    fetch(`/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(`✅ Лайк успешно обработан. Текущее количество лайков: ${data.total_likes}`);

        const likeCountElement = document.getElementById(`like-count-${postId}`);
        if (likeCountElement) {
            likeCountElement.innerText = data.total_likes;
        }

        // 🔥 Обновляем кнопку лайка
        let button = document.querySelector(`.like-button[data-post-id="${postId}"]`);
        if (button) {
            button.classList.toggle("btn-outline-primary", !data.liked);
            button.classList.toggle("btn-primary", data.liked);
        }
    })
    .catch(error => console.error('❌ Ошибка лайка:', error));
}

// ✅ Функция подписки/отписки (исправлено!)
window.toggleFollow = function (event, button) {
    event.preventDefault();  // Останавливаем стандартное поведение кнопки

    let userId = button.dataset.userId;
    if (!userId) {
        console.error("❌ Ошибка: userId не определён.");
        return;
    }

    let isFollow = button.dataset.following === "false";
    let url = isFollow ? `/users/follow/${userId}/` : `/users/unfollow/${userId}/`;

    console.log(`🟠 Отправка запроса: ${isFollow ? "Подписка" : "Отписка"} на пользователя ID ${userId}`);

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            console.log(`✅ Успешно: ${data.message}`);

            // 🔥 Обновляем количество подписчиков
            const followersCountElement = document.getElementById("followers-count");
            if (followersCountElement && data.followers_count !== undefined) {
                followersCountElement.innerText = data.followers_count;
            }

            // 🔥 Обновляем кнопку подписки/отписки без перезагрузки
            button.classList.toggle("btn-primary", !isFollow);
            button.classList.toggle("btn-danger", isFollow);
            button.innerText = isFollow ? "Отписаться" : "Подписаться";
            button.dataset.following = isFollow ? "true" : "false";
        } else {
            console.error(`❌ Ошибка: ${data.error}`);
        }
    })
    .catch(error => console.error("❌ Ошибка при подписке/отписке:", error));
};

// ✅ Проверяем подписки при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Скрипты загружены!");

    // 🔥 Исправляем подписку: привязываем toggleFollow к кнопкам
    document.querySelectorAll(".follow-button").forEach(button => {
        button.addEventListener("click", function (event) {
            toggleFollow(event, this);
        });
    });

    // ✅ Проверяем статус подписки
    document.querySelectorAll(".follow-button").forEach(button => {
        let userId = button.dataset.userId;
        if (!userId) {
            console.error("❌ Ошибка: отсутствует userId в data-user-id.");
            return;
        }

        fetch(`/users/check_follow_status/${userId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_following) {
                button.classList.replace("btn-primary", "btn-danger");
                button.innerText = "Отписаться";
                button.dataset.following = "true";
            } else {
                button.classList.replace("btn-danger", "btn-primary");
                button.innerText = "Подписаться";
                button.dataset.following = "false";
            }
        })
        .catch(error => console.error("❌ Ошибка получения статуса подписки:", error));
    });

    // ✅ Проверяем, загружен ли Bootstrap
    if (typeof bootstrap === "undefined") {
        console.error("❌ Ошибка: Bootstrap не загружен! Проверь подключение в `base.html`.");
    }
});

