window.addEventListener ("load", function() {
  document.querySelectorAll("input[value^='choco install']").forEach(e => {
    const button = document.createElement("button")
    button.classList.add("btn", "btn-secondary")
    button.innerText = "Install"
    e.parentElement.appendChild(button)
    button.addEventListener('click', function() {
      const url = 'http://localhost:22567/?cmd=' + encodeURIComponent(e.getAttribute('value'))
      console.log(`Launching ${url}...`)
      fetch(url, {
        referrerPolicy: "origin",
        mode: 'no-cors'
      }).then(() => {
        alert("Install queued")
      })
    })
  })
})
