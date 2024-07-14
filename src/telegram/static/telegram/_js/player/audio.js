const audio = document.getElementById('audio')
const play_pause_button = document.getElementById('play-pause-button')
const progress_container = document.getElementById('progress-container')
const progress_bar = document.getElementById('progress-container__bar')


function playAudio(){
    const icon = play_pause_button.getElementsByTagName('i')[0]
    icon.classList.remove('fa-play')
    icon.classList.add('fa-pause')
    audio.play()
}


function pauseAudio(){
    const icon = play_pause_button.getElementsByTagName('i')[0]
    icon.classList.remove('fa-pause')
        icon.classList.add('fa-play')
        audio.pause()
}


function secondsConverter(seconds) {
    const one_hour = 3600
    const one_minute = 60
    let remaining = Math.round(seconds)
    let time = ""

    if (remaining > one_hour) {
        let hours = Math.floor(remaining/one_hour)
        time += hours < 10 ? `0${hours}:` : `${hours}:`
        remaining -= hours * one_hour
    }

    let minutes = Math.floor(remaining/one_minute)
    time += minutes < 10 ? `0${minutes}:` : `${minutes}:`
    remaining -= minutes * one_minute

    time += remaining < 10 ? `0${remaining}` : remaining

    return time
}

function update_timer_total_time()
{
    const timer_total_time = document.getElementById('timer__total-time')

    if (timer_total_time.innerText == "--:--")
        timer_total_time.innerText = secondsConverter(audio.duration)
}


// Event to play and pause audio
play_pause_button.addEventListener('click', (event)=>{
    if (!audio.paused && audio.duration > 0 ){
        // Audio is playing
        pauseAudio()
    } else {
        // Audio is not playing
        update_timer_total_time()
        playAudio()
    }
})


// Update total time of the timer
audio.addEventListener('loadedmetadata', ()=>{
    update_timer_total_time()
})


// Update audio time
audio.addEventListener('timeupdate', ()=>{
    document.getElementById('timer__current-time').innerText = secondsConverter(audio.currentTime)
})


// Update audio progress bar
audio.addEventListener('timeupdate', ()=>{
    const progress_percent = (audio.currentTime / audio.duration) * 100
    progress_bar.style.width = `${progress_percent}%`

    if (audio.currentTime == audio.duration)
    {
        pauseAudio()
        progress_bar.style.width = `0%`
    }
})

// Click on progress bar
progress_container.addEventListener('click', (event)=>{
    let { width } = progress_container.getBoundingClientRect()
    audio.currentTime = (event.offsetX / width) * audio.duration
})