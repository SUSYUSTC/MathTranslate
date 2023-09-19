document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.fluent-button');

    buttons.forEach(button => {
        button.addEventListener('mousedown', function () {
            button.style.transform = 'translateY(0) scale(0.98)';
        });

        button.addEventListener('mouseup', function () {
            button.style.transform = 'translateY(-3px) scale(1)';
        });

        button.addEventListener('mouseleave', function () {
            button.style.transform = 'translateY(0) scale(1)';
        });
    });
});
