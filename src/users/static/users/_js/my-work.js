// Add click event into each element of the sumary list with "click-go-to" attribute
const summary_list = document.getElementById('summary-list')
summary_list.querySelectorAll('li[click-go-to]').forEach((item)=>{
    item.addEventListener('click', function(event){
        const element_id =  event.currentTarget.getAttribute('click-go-to')
        const element = document.getElementById(element_id)
        window.scrollTo({ 
            top: element.offsetTop,
            behavior: 'smooth' 
        })

    })
})


// Go up arrow
const fixed_arrow_button = document.getElementById('fixed-arrow-button')
fixed_arrow_button.addEventListener('click', (event)=>{
    window.scrollTo({ 
        top: 0,
        behavior: 'smooth' 
    })
})

const callback = (entries, observer) => {
    let display_style
    entries.forEach((entry) => {
        display_style = entry.isIntersecting ? 'none' : 'initial'
        fixed_arrow_button.style.display = display_style
    });
}
const observer = new IntersectionObserver(callback, {threshold: 1})
observer.observe(
    document.getElementById('summary-list')
)
