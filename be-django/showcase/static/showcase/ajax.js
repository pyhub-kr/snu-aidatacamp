function getContents (code) {
  fetch('/showcase/ajax.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const api = data.find(api => api.code === code);
    document.querySelectorAll('#contents nav ul li')
    .forEach(li => {li.classList.remove('selected')})

    document.querySelector(`#contents nav ul li.${code}`)
    .classList.add('selected');

    document.querySelector('#contents h2')
    .textContent = api.name;

    document.querySelector('#contents p')
    .textContent = api.content;
  })
  .catch(error => {
    console.error('Error ocurred:', error);
  });
}

document.querySelectorAll('#contents ul li')
.forEach(li => {
  li.addEventListener('click', function(e) {
    const code = Array.from(e.target.classList)
    .find(c => { return c != 'selected' })
    getContents(code);
  });
});

getContents('restapi');