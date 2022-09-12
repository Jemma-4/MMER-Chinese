export default {
    init () {
        let sw = document.documentElement.clientWidth
        if (sw > 550) {
            sw = 550
        }
        document.documentElement.style.fontSize = sw / 375 * 1.25 * 100 + '%'
        window.addEventListener("onorientationchange" in window ? "orientationchange" : "resize", function () {
            location.reload()
        }, false)
    }
}