document.addEventListener('DOMContentLoaded', () => {
    // Determine HTTP vs HTTPS protocol for WebSockets
    const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsUrl = wsProtocol + window.location.host + '/ws/keypress/';

    // Open connection
    const socket = new WebSocket(wsUrl);

    // DOM Element references
    const statusBadge = document.getElementById('status-badge');
    const displayKey = document.getElementById('display-key');
    const totalCount = document.getElementById('total-count');
    const logList = document.getElementById('log');

    // 1. Connection events
    socket.onopen = () => {
        statusBadge.textContent = 'Connected';
        statusBadge.className = 'status online';
    };

    socket.onclose = () => {
        statusBadge.textContent = 'Disconnected';
        statusBadge.className = 'status offline';
    };

    // 2. Receive data FROM consumers.py
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Update single DOM text nodes
        if (data.key) displayKey.textContent = data.key;
        if (data.total_count !== undefined) totalCount.textContent = data.total_count;

        // Prepend new item to the activity log
        if (data.time && data.key) {
            const li = document.createElement('li');
            li.textContent = `[${data.time}] Server recognized key: "${data.key}"`;
            logList.insertBefore(li, logList.firstChild);
        }
    };

    // 3. Send keypress events TO consumers.py
    document.addEventListener('keydown', (event) => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                'key': event.key
            }));
        }
    });
});