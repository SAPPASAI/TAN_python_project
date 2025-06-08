new WOW().init();
  
  // Smooth hover effects for map
  document.querySelectorAll('.map-container').forEach(map => {
    map.addEventListener('mouseenter', function() {
      this.querySelector('.map-iframe').style.transform = 'scale(1.02)';
    });
    
    map.addEventListener('mouseleave', function() {
      this.querySelector('.map-iframe').style.transform = 'scale(1)';
    });
  });


  