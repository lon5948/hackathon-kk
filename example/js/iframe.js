// IFrame window
window.addEventListener('message', event => {
  if (event.data.command === 'ping') {
    Array.from(document.querySelectorAll('iframe')).forEach(iframe =>
      iframe?.contentWindow?.postMessage({ command: 'pong' }, '*')
    );
  }
});