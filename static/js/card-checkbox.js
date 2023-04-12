const cardCheckboxes = document.querySelectorAll(".checkbox-card:not(.radio)");
const cardRadios = document.querySelectorAll(".checkbox-card.radio");


cardCheckboxes.forEach(cardCheckbox => {
    const input = cardCheckbox.querySelector("input");

    cardCheckbox.onclick = () => {
        input.checked = !input.checked
    }

    input.onfocus = (e) => {
        e.preventDefault();
        cardCheckbox.focus();
    }

    cardCheckbox.onkeyup = (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            // User pressed Enter key or spacebar.
            input.checked = !input.checked;
        }
    }
})

cardRadios.forEach(cardRadio => {
    const input = cardRadio.querySelector("input");

    cardRadio.onclick = () => {
        input.checked = true;
    }
    
    input.onfocus = (e) => {
        e.preventDefault();
        cardRadio.focus();
    }

    cardRadio.onkeyup = (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            // User pressed Enter key or spacebar.
            input.checked = true;
        }
    }
})

document.addEventListener('keydown', function(event) {
    const isTyping = event.target.classList.contains("checkbox-card");
    
    if (event.key === " " && isTyping) {
      event.preventDefault();
      // User pressed Enter key or spacebar.
    }
  });