document.getElementById('back-button').addEventListener('click', ()=>{
    history.back()
})


document.querySelectorAll('#setting-buttons > button[url]').forEach(element=>{
    element.addEventListener('click', ()=>{
        let url = element.getAttribute('url')
        window.open(url,'_blank');
        setTimeout(function(){
            window.location.reload()
        }, 2000)
    })
})