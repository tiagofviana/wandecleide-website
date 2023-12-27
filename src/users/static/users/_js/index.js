document.getElementById('view-1__background-video').playbackRate = 0.90

document.getElementById('scroll_button_1').addEventListener('click', ()=>{
    window.scrollTo({
        top: document.getElementById('view-2').offsetTop,
        behavior: 'smooth'
    })
})
