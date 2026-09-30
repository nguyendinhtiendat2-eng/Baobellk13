<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Đua Vịt Chọn Người Thắng</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 20px;
        }

        h1 {
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        #setup-container {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            display: inline-block;
            margin-bottom: 20px;
            backdrop-filter: blur(5px);
        }

        input, button {
            padding: 10px 15px;
            font-size: 16px;
            border-radius: 6px;
            border: none;
            margin: 5px;
        }

        input {
            width: 300px;
        }

        button {
            background-color: #00b894;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }

        button:hover {
            background-color: #55efc4;
            color: #2d3436;
        }

        #track-container {
            position: relative;
            background: #2d3436;
            border-radius: 15px;
            max-width: 900px;
            margin: 0 auto;
            overflow: hidden;
            border: 4px solid #dfe6e9;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            display: none;
        }

        .lane {
            border-bottom: 2px dashed rgba(255, 255, 255, 0.2);
            padding: 15px 10px;
            position: relative;
            min-height: 50px;
            display: flex;
            align-items: center;
        }

        .lane:last-child {
            border-bottom: none;
        }

        .finish-line {
            position: absolute;
            right: 80px;
            top: 0;
            bottom: 0;
            width: 6px;
            background: repeating-linear-gradient(0deg, #ff7675, #ff7675 10px, #dfe6e9 10px, #dfe6e9 20px);
            z-index: 1;
        }

        .duck {
            position: absolute;
            left: 10px;
            font-size: 28px;
            transition: transform 0.1s linear;
            z-index: 2;
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.9);
            color: #2d3436;
            padding: 2px 8px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }

        .duck span.icon {
            font-size: 22px;
            margin-right: 5px;
        }

        #winner-banner {
            display: none;
            margin-top: 20px;
            font-size: 24px;
            font-weight: bold;
            background: #fdcb6e;
            color: #2d3436;
            padding: 15px;
            border-radius: 10px;
            animation: bounce 0.5s infinite alternate;
        }

        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-5px); }
        }
    </style>
</head>
<body>

    <h1>🦆 Cuộc Đua Vịt Định Mệnh 🦆</h1>
    
    <div id="setup-container">
        <p>Nhập tên các người chơi/vịt (cách nhau bằng dấu phẩy):</p>
        <input type="text" id="player-input" value="An, Bình, Châu, Dương, Linh">
        <br>
        <button onclick="initGame()">Bắt đầu cuộc đua</button>
    </div>

    <div id="track-container">
        <div class="finish-line"></div>
        <div id="lanes"></div>
    </div>

    <div id="winner-banner"></div>

    <script>
        let isRacing = false;

        function initGame() {
            if (isRacing) return;

            const inputVal = document.getElementById('player-input').value.trim();
            if (!inputVal) {
                alert('Vui lòng nhập ít nhất một người chơi!');
                return;
            }

            const names = inputVal.split(',').map(name => name.trim()).filter(name => name.length > 0);
            if (names.length < 2) {
                alert('Cần ít nhất 2 người chơi để tổ chức cuộc đua!');
                return;
            }

            document.getElementById('winner-banner').style.display = 'none';
            const trackContainer = document.getElementById('track-container');
            const lanesContainer = document.getElementById('lanes');
            lanesContainer.innerHTML = '';
            trackContainer.style.display = 'block';

            const trackWidth = trackContainer.clientWidth - 120; // Trừ khoảng cách vạch đích
            let ducks = [];

            names.forEach((name, index) => {
                // Tạo đường đua
                const lane = document.createElement('div');
                lane.className = 'lane';
                
                // Tạo chú vịt
                const duck = document.createElement('div');
                duck.className = 'duck';
                duck.innerHTML = `<span class="icon">🦆</span> ${name}`;
                duck.style.left = '10px';
                
                lane.appendChild(duck);
                lanesContainer.appendChild(lane);

                ducks.push({
                    element: duck,
                    pos: 10,
                    speed: 0,
                    name: name
                });
            });

            startRace(ducks, trackWidth);
        }

        function startRace(ducks, trackWidth) {
            isRacing = true;
            let winnerFound = false;

            function update() {
                if (!isRacing) return;

                let allFinished = false;

                ducks.forEach(duck => {
                    if (!winnerFound) {
                        // Tăng tốc độ ngẫu nhiên cho mỗi khung hình
                        duck.speed = Math.random() * 4 + 1.5;
                        duck.pos += duck.speed;

                        if (duck.pos >= trackWidth) {
                            duck.pos = trackWidth;
                            winnerFound = true;
                            declareWinner(duck.name);
                        }
                    }
                    duck.element.style.left = duck.pos + 'px';
                });

                if (!winnerFound) {
                    requestAnimationFrame(update);
                } else {
                    isRacing = false;
                }
            }

            requestAnimationFrame(update);
        }

        function declareWinner(winnerName) {
            const banner = document.getElementById('winner-banner');
            banner.innerHTML = `🎉 Chúc mừng ${winnerName} đã giành chiến thắng! 🎉`;
            banner.style.display = 'block';
        }
    </script>
</body>
</html>
