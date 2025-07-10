class CustomAudioPlayer {
    #current_audio_index = 0

    constructor() {
        this.audios = document.getElementById('player').getElementsByTagName('audio')
        this.play_pause_button = document.getElementById('play-pause-button')        
        this.current_audio_title = document.getElementById('current-audio-title')
        this.audio_number = document.getElementById('audio-number')
        this.timer_total_time = document.getElementById('timer__total-time')
    }


    getCurrentAudio() {
        return this.audios[this.#current_audio_index]
    }


    playCurrentAudio() {
        const icon = this.play_pause_button.getElementsByTagName('i')[0]
        if (icon.classList.contains('fa-play')) {
            icon.classList.remove('fa-play')
            icon.classList.add('fa-pause')
            this.getCurrentAudio().play()

            console.log(`Play audio ${this.#current_audio_index}`)
        }

        if (this.timer_total_time.innerText == "--:--")
            this.#updateTimerTotalTime()
    }


    pauseCurrentAudio() {
        const icon = this.play_pause_button.getElementsByTagName('i')[0]
        if (icon.classList.contains('fa-pause')) {
            icon.classList.remove('fa-pause')
            icon.classList.add('fa-play')
            this.getCurrentAudio().pause()

            console.log(`Pause audio ${this.#current_audio_index}`)
        }
    }


    createEventListeners(){
        // Update total time of the timer
        this.getCurrentAudio().addEventListener('loadedmetadata', ()=>{
            this.#updateTimerTotalTime()
        }, { once: true })

        this.#createPlayPauseEvent()
        this.#createForwardEvent()
        this.#createBackardEvent()
        this.#createAudioEvent()
        this.#createProgressBarEvent()
        this.#createMusicListEvent()
    }


    #updateCurrentTime(audio){
        //Update current time
        let current_time = this.#secondsConverter(audio.currentTime)
        document.getElementById('timer__current-time').innerText = current_time
    }


    #updateProgressBar(audio){
        // Update progress bar
        let progress_bar = document.getElementById('progress-container__bar')
        let progress_percent = (audio.currentTime / audio.duration) * 100
        progress_bar.style.width = `${progress_percent}%`
    }


    #createAudioEvent(){
        for (let index = 0; index < this.audios.length; index++) {
            let audio = this.audios[index]
            audio.addEventListener('timeupdate', ()=>{
                this.#updateCurrentTime(audio)
                this.#updateProgressBar(audio)

                if (audio.currentTime == audio.duration) {
                    this.#goNextPreviousAudio(true)
                    this.playCurrentAudio()
                }
            })
        }
    }


    #createPlayPauseEvent() {
        this.play_pause_button.addEventListener('click', (event)=>{
            if (!this.getCurrentAudio().paused){
                // Audio is playing
                this.pauseCurrentAudio()
            } else {
                // Audio is not playing
                this.playCurrentAudio()
            }
        })
    }


    #updatePlayerData() {
        this.#updateTimerTotalTime()
        this.current_audio_title.innerText = this.getCurrentAudio().getAttribute('title')
        this.audio_number.innerText = this.#current_audio_index + 1
    }

    
    /**
     * @param {Boolean} is_next true to go to the next song
     */
    #goNextPreviousAudio(is_next){
        const current_audio = this.getCurrentAudio()
        const was_playing = !current_audio.paused
        this.pauseCurrentAudio()
        current_audio.currentTime = 0

        let index = this.#current_audio_index
        index += is_next ?  1 : -1

        if(typeof this.audios[index] === 'undefined')
            index = is_next ? 0 : this.audios.length - 1

        this.#current_audio_index = index
        this.#updatePlayerData()
        if (was_playing) this.playCurrentAudio()
        console.log(`Changing to audio ${this.#current_audio_index}`)
    }


    #createForwardEvent(){
        document.getElementById('forward-button').addEventListener('click', (event)=>{
           this.#goNextPreviousAudio(true)
        })
    }

    
    #createBackardEvent(){
        document.getElementById('backward-button').addEventListener('click', (event)=>{
            this.#goNextPreviousAudio(false)
        })
    }


    #secondsConverter(seconds) {
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


    #updateTimerTotalTime()
    {
        const total_time = this.#secondsConverter(this.getCurrentAudio().duration)
        this.timer_total_time.innerText = total_time
        console.log(`Updating total time of the timer: ${total_time}`)
    }

    
    #createProgressBarEvent(){
        // Click on progress bar
        const progress_container = document.getElementById('progress-container')

        progress_container.addEventListener('click', (event)=>{
            const current_audio = this.getCurrentAudio()
            let { width } = progress_container.getBoundingClientRect()
            current_audio.currentTime = (event.offsetX / width) * current_audio.duration
        })
    }


    #createMusicListEvent(){
        const list_items = document.getElementById('audio_title_list')?.getElementsByTagName('li')
        if (list_items == null) return

        for(let index= 0; index < list_items.length; index++) {
            list_items[index].addEventListener('click', (event)=>{
                const current_audio = this.getCurrentAudio()
                this.pauseCurrentAudio()
                current_audio.currentTime = 0
                
                const audio_element_id = event.target.getAttribute('audio_element_id')
                const audio_to_set = document.getElementById(audio_element_id)
                if (audio_to_set != null) {
                    this.#current_audio_index = Array.from(audio_to_set.parentNode.children).indexOf(audio_to_set)
                    this.#updatePlayerData()
                    this.playCurrentAudio()
                }

            })
        }
    }

}

const player = new CustomAudioPlayer()
player.createEventListeners()