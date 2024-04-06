let button = document.getElementById('scrapy_bvids')
button.addEventListener('click', () => {
    console.log("clicked")
    let html = document.querySelector("body > gradio-app > div").innerHTML
    console.log(html)
})

window.wzq = 123