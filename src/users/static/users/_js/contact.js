document.getElementById('phone-container').addEventListener('click', (event) => {
    const phone_number = document.getElementById('phone-container__number').textContent
    document.getElementById('copied-message').style.visibility = 'visible'
    navigator.clipboard.writeText(phone_number);
})
