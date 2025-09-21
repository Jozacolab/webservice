window.addEventListener('load', () => {
  const canvas = document.getElementById("bg");
  const ctx = canvas.getContext("2d");

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);

  const mouse = { x: null, y: null, radius: 120 };
  window.addEventListener("mousemove", (e) => { mouse.x = e.x; mouse.y = e.y; });

  class Particle {
    constructor(x, y, size, speedX, speedY) {
      this.x = x;
      this.y = y;
      this.size = size;
      this.speedX = speedX;
      this.speedY = speedY;
    }

    update() {
      this.x += this.speedX;
      this.y += this.speedY;

      if (this.x + this.size > canvas.width || this.x - this.size < 0) this.speedX *= -1;
      if (this.y + this.size > canvas.height || this.y - this.size < 0) this.speedY *= -1;

      const dx = mouse.x - this.x;
      const dy = mouse.y - this.y;
      const distance = Math.sqrt(dx*dx + dy*dy);

      if (distance < mouse.radius) {
        const angle = Math.atan2(dy, dx);
        const force = (mouse.radius - distance) / mouse.radius;
        this.x -= Math.cos(angle) * force * 4;
        this.y -= Math.sin(angle) * force * 4;
      }
    }

    draw() {
      ctx.fillStyle = "rgba(255,255,255,0.8)";
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  let particlesArray = [];
  function initParticles() {
    particlesArray = [];
    for (let i = 0; i < 150; i++) {
      const size = Math.random() * 3 + 1;
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      const speedX = (Math.random() - 0.5) * 2;
      const speedY = (Math.random() - 0.5) * 2;
      particlesArray.push(new Particle(x, y, size, speedX, speedY));
    }
  }
  initParticles();

  function connect() {
    for (let a = 0; a < particlesArray.length; a++) {
      for (let b = a; b < particlesArray.length; b++) {
        const dx = particlesArray[a].x - particlesArray[b].x;
        const dy = particlesArray[a].y - particlesArray[b].y;
        const dist = dx*dx + dy*dy;
        if (dist < 9000) {
          ctx.strokeStyle = 'rgba(255,255,255,0.1)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
          ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particlesArray.forEach(p => { p.update(); p.draw(); });
    connect();
    requestAnimationFrame(animate);
  }

  animate();
});
