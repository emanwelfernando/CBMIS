  function closeModal() {
    const modal = document.getElementById('addMunicipal');
    modal.classList.remove('fade-in');
    modal.classList.add('fade-out');
    setTimeout(function() {
      modal.style.display = 'none';
      modal.classList.remove('fade-out');
    }, 300); // Adjust the duration (300ms) to match your animation time
  }
