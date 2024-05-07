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


// Like and dislike counters
class LikeDislikeCounter
{
    constructor(id, like_button_elmt, dislike_button_elmt)
    {
        this.id = id
        this.like_button_elmt = like_button_elmt
        this.dislike_button_elmt = dislike_button_elmt
    }

    like()
    {
        if (this.#isValidCookie('like'))
        {
            this.#appendLike(-1)
            this.#deleteCookie()
            this.#notify(false, 'remove-like')
            this.like_button_elmt.removeAttribute('checked')
            this.like_button_elmt.parentElement.parentElement.querySelector('[message]').style.visibility = 'hidden'
            return
        }
        
        const is_update = this.#isValidCookie('')

        if (this.#isValidCookie('dislike'))
        {
            this.#appendDislike(-1)
            this.dislike_button_elmt.removeAttribute('checked')
        }

        this.#createCookie('like')
        this.#notify(is_update, 'like')
        this.#appendLike(1)
        this.like_button_elmt.setAttribute('checked', true)
        this.like_button_elmt.parentElement.parentElement.querySelector('[message]').style.visibility = 'visible'
    }
    
    dislike()
    {
        if (this.#isValidCookie('dislike'))
        {
            this.#deleteCookie()
            this.#appendDislike(-1)
            this.#notify(false, 'remove-dislike')
            this.dislike_button_elmt.removeAttribute('checked')
            this.dislike_button_elmt.parentElement.parentElement.querySelector('[message]').style.visibility = 'hidden'
            return
        }
        
        const is_update = this.#isValidCookie('')

        if (this.#isValidCookie('like'))
        {
            this.#appendLike(-1)
            this.like_button_elmt.removeAttribute('checked')
        }

        this.#createCookie('dislike')
        this.#notify(is_update, 'dislike')
        this.#appendDislike(1)
        this.dislike_button_elmt.setAttribute('checked', true)
        this.dislike_button_elmt.parentElement.parentElement.querySelector('[message]').style.visibility = 'visible'
    }

    #appendLike(number)
    {
        const like_counter_elmt = this.like_button_elmt.querySelector('[like_counter]')
        let counter = parseInt(like_counter_elmt.innerText, 10) + number
        like_counter_elmt.innerText = counter
    }

    #appendDislike(number)
    {
        const dislike_counter_elmt = this.dislike_button_elmt.querySelector('[dislike_counter]')
        let counter = parseInt(dislike_counter_elmt.innerText, 10) + number
        dislike_counter_elmt.innerText = counter
    }

    #isValidCookie(data)
    {
        const name = this.#createCookieName()
        return document.cookie.includes(`${name}=${data}`)
    }

    #createCookieName()
    {
        return "like_dislike_" + this.id
    }

    #createCookieExpires()
    {
        const date = new Date();
        const year = date.getFullYear() + 1 // one year from now
        date.setFullYear(year)
        return "expires=" + date.toUTCString()
    }

    #createCookie(data)
    {
        const name = this.#createCookieName()
        const expires = this.#createCookieExpires()
        document.cookie = `${name}=${data};path=/; ${expires}`
    }

    #deleteCookie()
    {
        const name = this.#createCookieName()
        document.cookie = `${name}=;path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT`
    }

    #notify(is_update, reply)
    {
        let xmlHttp = new XMLHttpRequest()

        is_update = (is_update === true) ? 1 : 0
        
        const url = `/like-dislike/${this.id}/${reply}/${is_update}/`
        const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
        
        xmlHttp.open('POST', url, true)
        xmlHttp.setRequestHeader('X-CSRFToken', csrftoken)
        xmlHttp.send()
    }
}

document.querySelectorAll('[like_dislike_counter_id]').forEach((item) => {
    const like_button_elmt = item.querySelector('[like_button]')
    const dislike_button_elmt = item.querySelector('[dislike_button]')
    const counter_id = item.getAttribute('like_dislike_counter_id')
    const counter = new LikeDislikeCounter(counter_id, like_button_elmt, dislike_button_elmt)

    like_button_elmt.addEventListener('click', (event) => {
        counter.like()
    })

    dislike_button_elmt.addEventListener('click', (event) => {
        counter.dislike()
    })
})
