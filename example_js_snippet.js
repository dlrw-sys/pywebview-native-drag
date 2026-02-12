let isNativeDragging = false;

li.onmousedown = e => {
    if (e.button !== 0) return;

    const startX = e.screenX;
    const startY = e.screenY;

    const handleMove = moveEvent => {

        if (Math.abs(moveEvent.screenX - startX) > 15 ||
            Math.abs(moveEvent.screenY - startY) > 15) {

            if (isNativeDragging) return;
            isNativeDragging = true;

            document.removeEventListener('mousemove', handleMove);

            const selection = selectionMap[side];

            console.log('[NATIVE DRAG] Calling Python');

            window.pywebview.api.external_drag({
                paths: [...selection],
                ctrl: e.ctrlKey
            }).finally(() => {
                console.log('[NATIVE DRAG] finished');
                isNativeDragging = false;
            });
        }
    };

    const handleUp = () => {
        document.removeEventListener('mousemove', handleMove);
        document.removeEventListener('mouseup', handleUp);
    };

    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
};
