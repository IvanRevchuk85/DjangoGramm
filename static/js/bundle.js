/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./frontend/src/main.js":
/*!******************************!*\
  !*** ./frontend/src/main.js ***!
  \******************************/
/***/ (() => {

eval("// Получаем CSRF-токен из скрытого input в шаблоне\nvar csrfToken = document.getElementById('csrf-token') ? document.getElementById('csrf-token').value : null;\n\nconsole.log(\"✅ CSRF-токен:\", csrfToken);  // <-- Проверка, загружается ли токен\n\nif (!csrfToken) {\n    console.error(\"❌ Ошибка: CSRF-токен не найден! Проверь HTML-код.\");\n}\n\n// Функция для лайка\nfunction toggleLike(postId) {\n    console.log(`🟢 Отправка запроса на лайк для поста ID: ${postId}`);\n\n    fetch(`/posts/${postId}/like/`, {\n        method: 'POST',\n        headers: {\n            'X-CSRFToken': csrfToken,\n            'Content-Type': 'application/json'\n        }\n    })\n        .then(response => {\n            console.log(`🔵 Ответ сервера (лайк): ${response.status}`);\n            if (!response.ok) {\n                throw new Error(`Ошибка HTTP: ${response.status}`);\n            }\n            return response.json();\n        })\n        .then(data => {\n            console.log(`✅ Лайк успешно обработан. Текущее количество лайков: ${data.total_likes}`);\n\n            const likeCountElement = document.getElementById(`like-count-${postId}`);\n            if (likeCountElement) {\n                likeCountElement.innerText = data.total_likes;\n            }\n        })\n        .catch(error => console.error('❌ Ошибка лайка:', error));\n}\n\n// Функция для подписки и отписки\ndocument.addEventListener(\"DOMContentLoaded\", function () {\n    document.querySelectorAll(\".follow-form\").forEach(form => {\n        form.addEventListener(\"submit\", function (event) {\n            event.preventDefault();  // Блокируем стандартную отправку формы\n\n            let userId = this.dataset.userId;  // Получаем ID пользователя\n            let button = this.querySelector(\"button\");\n\n            console.log(`🟡 Запрос на подписку/отписку. userId: ${userId}`);\n\n            if (!userId || isNaN(userId)) {\n                console.error(\"❌ Ошибка: user_id не определен или не является числом!\");\n                return;\n            }\n\n            let isFollow = button.innerText.trim() === \"Подписаться\";  // Определяем, подписка или отписка\n            let url = isFollow ? `/users/follow/${userId}/` : `/users/unfollow/${userId}/`;\n\n            console.log(`🟠 Отправка запроса: ${isFollow ? \"Подписка\" : \"Отписка\"} на пользователя ID ${userId}`);\n\n            fetch(url, {\n                method: \"POST\",\n                headers: {\n                    \"X-CSRFToken\": csrfToken,\n                    \"Content-Type\": \"application/json\"\n                },\n            })\n                .then(response => response.json())\n                .then(data => {\n                    if (data.message) {\n                        console.log(`✅ Успешно: ${data.message}`);\n\n                        // Обновляем количество подписчиков\n                        const followersCountElement = document.getElementById(\"followers-count\");\n                        if (followersCountElement) {\n                            followersCountElement.innerText = data.followers_count;\n                        }\n\n                        // Меняем кнопку подписки/отписки\n                        if (isFollow) {\n                            button.classList.replace(\"btn-primary\", \"btn-danger\");\n                            button.innerText = \"Отписаться\";\n                        } else {\n                            button.classList.replace(\"btn-danger\", \"btn-primary\");\n                            button.innerText = \"Подписаться\";\n                        }\n                    } else {\n                        console.error(`❌ Ошибка: ${data.error}`);\n                    }\n                })\n                .catch(error => console.error(\"❌ Ошибка при подписке/отписке:\", error));\n        });\n    });\n});\n\n\n//# sourceURL=webpack://task_14/./frontend/src/main.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./frontend/src/main.js"]();
/******/ 	
/******/ })()
;