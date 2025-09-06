const video = document.getElementById("videoInput");
const canvas = document.getElementById("canvasOutput");
canvas.width = 640;
canvas.height = 480;
const ctx = canvas.getContext("2d");
const detector = new AR.Detector();

let balanceCache = {};
let lastFetchTime = {};

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        document.getElementById("status").textContent = "カメラ準備完了。マーカーをかざしてください。";
        requestAnimationFrame(processVideo);
    })
    .catch(err => {
        document.getElementById("status").textContent = "カメラ取得失敗: " + err;
    });

function processVideo() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const markers = detector.detect(imageData);

    drawMarkers(markers);

    requestAnimationFrame(processVideo);
}

function drawMarkers(markers) {
    if (!markers || markers.length === 0) return;

    for (let i = 0; i < markers.length; i++) {
        const marker = markers[i];
        const corners = marker.corners;
        const markerId = marker.id;
        const color = i === 0 ? "green" : "red";

        ctx.beginPath();
        ctx.moveTo(corners[0].x, corners[0].y);
        for (let j = 1; j < corners.length; j++) {
            ctx.lineTo(corners[j].x, corners[j].y);
        }
        ctx.closePath();
        ctx.lineWidth = 3;
        ctx.strokeStyle = color;
        ctx.stroke();

        const cx = (corners[0].x + corners[2].x) / 2;
        const cy = (corners[0].y + corners[2].y) / 2;

        const balance = balanceCache[markerId] ?? "...";

        ctx.font = "20px sans-serif";
        ctx.fillStyle = "green";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(`ID:${markerId} POINT:${balance}`, cx, cy);

        const now = Date.now();
        if (
            !lastFetchTime[markerId] ||
            now - lastFetchTime[markerId] > 2000
        ) {
            lastFetchTime[markerId] = now;
            getBalance(markerId).then(fetched => {
                balanceCache[markerId] = fetched;
            });
        }
    }
}


async function getCachedBalance(id) {
    const now = Date.now();
    if (
        !balanceCache[id] ||
        !lastFetchTime[id] ||
        now - lastFetchTime[id] > 1000
    ) {
        const balance = await getBalance(id);
        balanceCache[id] = balance ?? 0;
        lastFetchTime[id] = now;
    }
    return balanceCache[id];
}

async function getBalance(id) {
    try {
        const res = await fetch("/users/get-balance", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id })
        });

        console.log("API:", res);

        if (!res.ok) {
            const error_message = `ERROR: ${res.status} ${res.statusText}`;
            console.warn(error_message);
            document.getElementById("status").textContent = error_message;
            return 0;
        }

        const data = await res.json();
        console.log("API:", data);
        return parseFloat(data.balance);
    } catch (err) {
        const error_message = "fetch: " + err;
        console.error(error_message);
        document.getElementById("status").textContent = error_message;
        return 0;
    }
}
