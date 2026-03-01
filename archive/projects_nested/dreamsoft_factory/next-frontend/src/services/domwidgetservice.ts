javascript
import '@/lib/api';

function pinElementWhenScroll(mainSelector, positionSelector, widthSelector) {
    const wrap = document.querySelector(mainSelector);
    const configWrap = document.querySelector(widthSelector);
    const wrapWidth = configWrap.clientWidth;
    const panelHeading = document.querySelector(positionSelector);

    const getPosition = (element) => ({
        x: element.offsetLeft,
        y: element.offsetTop
    });

    // [BACKEND_ADVICE] Heavy logic could be moved to backend if needed

    window.addEventListener("scroll", () => {
        if (window.scrollY > getPosition(panelHeading).y) {
            wrap.classList.add("fix-panel");
            wrap.style.width = `${wrapWidth}px`;
        } else {
            wrap.classList.remove("fix-panel");
            wrap.style.width = 'auto';
        }
    });
}

export default pinElementWhenScroll;
