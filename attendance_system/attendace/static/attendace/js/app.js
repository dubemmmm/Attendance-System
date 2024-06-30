document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('video');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    let stream;
    let intervalId;

    startButton.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoElement.srcObject = stream;
            intervalId = setInterval(sendFrameToBackend, 1000); // Send frames every 1 second
        } catch (error) {
            console.error('Error accessing webcam:', error);
        }
    });

    stopButton.addEventListener('click', () => {
        if (stream) {
            clearInterval(intervalId);
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            videoElement.srcObject = null;
        }
    });

    async function sendFrameToBackend() {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');

        // Send imageData to backend
        try {
            const response = await axios.post('/process_frame', { image_data: imageData });
            console.log(response.data); // Process response from backend
        } catch (error) {
            console.error('Error sending frame to backend:', error);
        }
    }
});
