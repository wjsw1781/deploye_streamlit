window.onload = () => {

    console.log("aa.js loaded")
    console.log("get_bvids")
    let html = document.querySelector("body > gradio-app > div").innerHTML
    console.log(html)

    button = document.getElementById('scrapy_bvids')
    
    console.log("🚀 ~ button:", button)
    
    button?.addEventListener('click', () => {
        debugger
        console.log("clicked")
        let html = document.querySelector("body > gradio-app > div").innerHTML
        console.log(html)
    })


}







