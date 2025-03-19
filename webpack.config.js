const path = require('path');

module.exports = {
    entry: './frontend/src/index.js',  // Входной файл
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/frontend'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,  // 🔥 Добавляем поддержку JS
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"]
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.scss$/,  // ✅ Исправлен синтаксис регулярки
                use: ['style-loader', 'css-loader', 'sass-loader'],
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.json', '.scss', '.css']
    }
};
