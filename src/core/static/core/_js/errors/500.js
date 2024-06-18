function createFrontDrop(left, bottom, rand)
{
    // rand must a number between 1 and 98
    return ` 
        <div 
            class="drop" 
            style="left: ${left}%; bottom: ${bottom}%; animation-delay: 0.${rand}s; animation-duration: 0.5${rand}s;"
        >
            <div 
                class="water"
                style="animation-delay: 0.${rand}s; animation-duration: 0.5${rand}s;"
            ></div>

            <div 
                class="splat"
                style="animation-delay: 0.${rand}s; animation-duration: 0.5${rand}s;"
            >
            </div>
        </div>
    `
}


function createBackDrop(right, bottom, rand)
{
    // rand must a number between 1 and 98
    return ` 
        <div
            class="drop"
            style="right:  ${right}%; bottom: ${bottom}%; animation-delay: 0.${rand}s; animation-duration: 0.5${rand}s;"
        >
            <div 
                class="water"
                style="animation-delay: 0.${rand}s; animation-duration: 0.5${rand}s;"
            ></div>

            <div 
                class="splat"
                style="animation-delay: 0.${rand}s; animation-duration: 0.5${rand}s;"
            >
            </div>
        </div>
    `
}


function createRain(){
    let front_drops = ""
    let back_drops = ""
    let increment = 0

    while (increment < 98) {
        //couple random numbers to use for various randomizations
    
        //random number between 98 and 1
        let random_1_to_98 = (Math.floor(Math.random() * (98 - 1 + 1) + 1))
        //random number between 5 and 2
        let random_2_to_5 = (Math.floor(Math.random() * (5 - 2 + 1) + 2))
        let position =  random_2_to_5 + random_2_to_5 - 1 + 100
        
        increment += random_2_to_5
    
        front_drops += createFrontDrop(increment, position, random_1_to_98)
        back_drops += createBackDrop(increment, position, random_1_to_98)
    
    }

    document.getElementById('rain').getElementsByClassName('front-row')[0].innerHTML = front_drops
    document.getElementById('rain').getElementsByClassName('back-row')[0].innerHTML = back_drops
}


createRain()