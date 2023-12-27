document.addEventListener('click', (event)=>{
    const menu = document.getElementById('menu') ?? null

    if (menu != null)
    {
        const is_contained = menu.contains(event.target)
        if (!is_contained) {
            document.getElementById('menu__hamburguer__checkbox').checked = false
            document.getElementById('menu__language__checkbox').checked = false
        }
    }
})

const menu_language_callback = (event) => {
    const current_language = document.getElementById('menu__languages__list').getAttribute('current-language')
    console.log(event.target)
}

document.querySelectorAll('#menu__languages__list > li').forEach(
    (element) => {
        element.addEventListener('click', menu_language_callback)
    }
)