document.querySelectorAll('*[role="alert"] > *[alert-delete]').forEach(alert => {
    alert.addEventListener('click', ()=>{
        alert.parentElement.remove()
    })
});