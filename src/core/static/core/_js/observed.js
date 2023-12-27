const callback = (entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting)
        {
            observer.unobserve(entry.target)
            entry.target.style.animationPlayState = 'running'            
            entry.target.addEventListener('animationend', () => {
                entry.target.style.opacity = '1'
            })
        }
    });
}
const observer = new IntersectionObserver(callback, {threshold: 1})

document.querySelectorAll('.observed').forEach(
    (element) => {
        if (has_animation(element))
        {
            element.style.opacity = '0'
            element.style.animationPlayState = 'paused'
            setTimeout(()=>{observer.observe(element)}, 1000)
        }
    }
)

function has_animation(element){
    const css_object = window.getComputedStyle(element, null);
    const animation_name = css_object.getPropertyValue('animation-name')    
    return (animation_name == 'none') ? false : true
}